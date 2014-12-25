from __future__ import absolute_import
import ftplib
from io import StringIO
import os

from celery import shared_task
from celery.utils.log import get_task_logger

import time
from datetime import datetime, timedelta
# from rest_framework.request import Request
from django.conf import settings
from django.core.cache import cache
import requests
import json
from message_converter.csv2json import Csv2Json
from message_converter.models import ConvertedMessageQueue, Project, LastDelivery, PullProject, LastPull, \
    IncomingMessage
from raven import Client as ravenClient
from time import sleep
import sys

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 10 # Lock expires in 10 minutes

@shared_task
def add(x, y):
    result = x + y

    logger.info('The result: %s' % result)
    return result


def reconvert_pulled_message(converted_message):
    convert_pulled_message(converted_message.original_message, converted_message)

def convert_pulled_message(original_message, converted_message=None):
    pull_project = original_message.project

    # convert from CSV to JSON
    outline = pull_project.conversion_parameters
    if outline:
        outline = json.loads(outline)
    csv2json = Csv2Json(outline)
    if pull_project.from_type.type_code == 'EDI945':
        converted = csv2json.convert_edi_945_to_wof_shipment(original_message.message)
    else:
        converted = csv2json.convert(original_message.message)

    if converted_message:
        converted_message.converted_message = converted
        converted_message.save()
        logger.info('Successfully reconverted message id: %s' % converted_message.id)
    else:
        converted_message = ConvertedMessageQueue.objects.create(original_message=original_message,
                                             converted_message=converted, project=pull_project)
        logger.info('Created message id: %s' % converted_message.id)


def _get_ftp_file_size(file, session):
    file_sizes = {}
    session.retrlines('LIST', lambda line: file_sizes.update({line.split()[-1]: int(line.split()[-5])}))
    return file_sizes.get(file)


class LockAccessError(Exception):
    pass


def acquire_lock(lock_id):
    # cache.add returns False if the key already exists, True if it doesn't, and 0 if the cache fails
    lock_result = cache.add(lock_id, 'true', LOCK_EXPIRE)
    if not isinstance(lock_result, bool):
        raise LockAccessError('Could not access the cache.')
    return lock_result


def release_lock(lock_id):
    # memcache delete is very slow, but we have to use it to take
    # advantage of using add() for atomic locking
    cache.delete(lock_id)

@shared_task
def pull_messages():
    """

    This should be scheduled as a periodic task

    """

    logger.info("Running pull_messages task.")

    for pull_project in PullProject.objects.filter(enabled=True):
        # read file into memory?
        # Pull file from FTP

        if not pull_project.pull_from_ftp:
            raise NotImplementedError('PullProject only supports pull_from_ftp')

        if pull_project.from_type.format != 'CSV':
            raise NotImplementedError('PullProject only supports CSV from_type')

        if pull_project.to_type.format != 'JSON':
            raise NotImplementedError('PullProject only supports JSON to_type')

        last_pull, created = LastPull.objects.get_or_create(pull_project=pull_project)

        span = datetime.now() - last_pull.last_pulled
        if span < timedelta(minutes=pull_project.pull_frequency):
            logger.info("Not ready to pull messages for %s project yet." % pull_project)
            continue  # not enough time has passed


        # lock pull project from running again
        lock_id = 'pull_project_lock-%s' % (pull_project.name)
        try:
            if not acquire_lock(lock_id):
                logger.info('Pull project task is already running for project %s' % pull_project.name)
                return
        except LockAccessError:
            logger.error('Could not acquire lock for pull project %s' % pull_project.name)
            raise

        logger.info("Pulling messages for %s project." % pull_project)

        session = ftplib.FTP(pull_project.pull_from_ftp.host, pull_project.pull_from_ftp.user, pull_project.pull_from_ftp.password)

        if pull_project.pull_from_ftp.path:
            working_path = pull_project.pull_from_ftp.path.strip()
            session.cwd(working_path)
        else:
            working_path = session.pwd()

        pull_count = 0
        file_type = '.' + pull_project.from_type.format.lower()

        for file in session.nlst():

            # TODO, add pattern matching
            if file.lower().endswith(file_type) or file.lower().endswith('.txt'):

                logger.info("Pulling message file: %s" % file)

                if pull_project.check_file_size_interval:
                    time_spent_waiting = 0
                    # check file size
                    old_size = _get_ftp_file_size(file, session)

                    # wait until the file stops being written to
                    while True:
                        # wait to check file size again
                        sleep(pull_project.check_file_size_interval)

                        time_spent_waiting += pull_project.check_file_size_interval

                        new_size = _get_ftp_file_size(file, session)
                        if old_size == new_size:
                            # file size not changing anymore, let's get out of here
                            logger.info('Waited %s seconds for %s to finish writing.' % (time_spent_waiting, file))
                            break

                        # never wait more than 5 minutes
                        if time_spent_waiting >= pull_project.max_file_size_wait_time:
                            error = 'Waited too long for file %s to finish being written to (%s seconds).' % (file, time_spent_waiting)
                            logger.error(error)
                            raise Exception(error)

                        old_size = new_size


                r = StringIO()
                # session.retrbinary('RETR ' + pull_project.pull_from_ftp.path, r.write)
                session.retrlines('RETR ' + file, lambda line: r.write('%s\n' % line))

                original_message = IncomingMessage.objects.create(project=pull_project, message=r.getvalue(), file_name=file)
                r.close()

                convert_pulled_message(original_message)

                logger.info("Finished converting message file: %s" % file)

                if pull_project.pull_from_ftp.delete_processed:
                    session.delete(file)
                    logger.info("Deleted message file: %s" % file)
                elif pull_project.pull_from_ftp.processed_path:

                    # Move file to processed folder
                    processed_path = pull_project.pull_from_ftp.processed_path.strip()

                    try:
                        session.cwd(processed_path)
                    except ftplib.error_perm as e:
                        if str(e) == '550 Failed to change directory.':
                            session.mkd(processed_path)
                    
                    session.cwd(working_path)
                    processed_file = processed_path + '/' + file
                    session.rename(file, processed_file)
                    logger.info("Moved message file to processed path: %s" % processed_file)

                pull_count += 1

        last_pull.save()
        logger.info("%s messages files pulled for %s project." % (pull_count, pull_project))
        release_lock(lock_id)



def get_messages(converted_message, messages_per_delivery):
    message_data = []
    first_index = 0
    last_index = messages_per_delivery
    if messages_per_delivery:
        data = json.loads(converted_message)
        for key in data:
            if isinstance(data[key], list):

                while True:
                    chunk = {key: data[key][first_index:last_index]}
                    if chunk[key]:
                        message_data.append(json.dumps(chunk))
                        first_index += messages_per_delivery
                        last_index += messages_per_delivery
                    else:
                        break
    if not message_data:
        message_data.append(converted_message)
    return message_data


def _send_to_api(project, undelivered):
    message_ids = []

    host = project.send_to_api.host

    headers = {'content-type': 'application/json'}

    # //request.add_header('X-Hub-Store', settings.X_Hub_Store)
    # request.add_header('X-Hub-Access-Token', settings.X_Hub_Access_Token)

    for header in project.send_to_api.apiheader_set.all():
        headers[header.name] = header.value

    for message in undelivered:


        try:
            message_data = get_messages(message.converted_message, project.messages_per_delivery)

            part = 1
            for data in message_data:
                logger.info('Sending part %s of %s for message id %s' % (part, len(message_data), message.id))
                response = requests.post(host, data, headers=headers)
                response.raise_for_status()
                part += 1

            message_ids.append(message.id)
            logger.info('Message id %s was fully delivered.' % (message.id,))
        except Exception as e:
            logger.error('Error delivering message id %s. Exception Type: %s, Exception: %s' % (message.id, type(e), e))
            ravenClient(dsn=getattr(settings, 'SENTRY_DSN', '')).captureException(extra={"message_id": message.id})

            if PullProject.objects.filter(id=project.id).exists():
                try:
                    # try to reconvert in case there is a new outline, or code change
                    logger.info('Reconverting message id: %s' % message.id)
                    reconvert_pulled_message(message)
                except:
                    logger.error('Failed reconverting message id: %s' % message.id)


    return message_ids


def _send_to_ftp(project, undelivered):

    logger.info('Default encoding: %s' % sys.getdefaultencoding())

    message_ids = []

    file_name = 'workfile-%s.txt' % time.strftime("%Y_%m_%d_%H_%M_%S")
    with open(file_name, 'w+', newline='\r\n') as f:
        for message in undelivered:
            f.write(message.converted_message)
            message_ids.append(message.id)

    # upload file to share
    with open(file_name, 'rb') as upload_file:
        session = ftplib.FTP(project.send_to_ftp.host, project.send_to_ftp.user, project.send_to_ftp.password)
        if project.send_to_ftp.path:
            path = project.send_to_ftp.path.strip()
            session.cwd(path)
        session.storlines('STOR ' + file_name, upload_file)
        session.quit()

    try:
        # delete work file
        os.remove(file_name)
    except Exception as e:
        logger.error('Could not remove work file: "%s". Exception Type: %s, Exception: %s' % (file_name, type(e), e))

    return message_ids


@shared_task
def deliver_messages():
    """

    This should be scheduled as a periodic task

    """

    logger.info("Running deliver_messages task.")

    for project in Project.objects.filter(enabled=True):

        last_delivery, created = LastDelivery.objects.get_or_create(project=project)

        span = datetime.now() - last_delivery.last_delivered
        if span < timedelta(minutes=project.delivery_frequency):
            logger.info("Not ready to deliver messages for %s project yet." % project)
            continue  # not enough time has passed

        undelivered = ConvertedMessageQueue.objects.filter(delivered=False, project=project).order_by('created')

        if project.delivery_message_age:
            newest_message_cutoff = datetime.now() - timedelta(project.delivery_message_age)
            # exclude anything that's too new
            undelivered = undelivered.exclude(created__gt=newest_message_cutoff)
            logger.info("Excluding messages newer than %s (%s minutes ago)" % (newest_message_cutoff, project.delivery_message_age))

        if not undelivered:
            logger.info("No messages to deliver for %s project." % project)
            continue

        try:
            if project.send_to_ftp:
                message_ids = _send_to_ftp(project, undelivered)
            else:
                message_ids = _send_to_api(project, undelivered)

            ConvertedMessageQueue.objects.filter(id__in=message_ids).update(delivered=True)
            last_delivery.save()  # update last_delivered time
            logger.info("%s messages delivered for %s project." % (len(message_ids), project))

        except Exception as e:
            logger.error('Error delivering messages for project id %s. Exception Type: %s, Exception: %s' % (project.id, type(e), e))
            if created:
                last_delivery.delete()







