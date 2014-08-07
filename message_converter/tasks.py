from __future__ import absolute_import
import ftplib
from io import StringIO
import os

from celery import shared_task
from celery.utils.log import get_task_logger

import time
from datetime import datetime, timedelta
# from rest_framework.request import Request
import requests
import json
from message_converter.csv2json import Csv2Json
from message_converter.models import ConvertedMessageQueue, Project, LastDelivery, PullProject, LastPull, \
    IncomingMessage

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    result = x + y

    logger.info('The result: %s' % result)
    return result

@shared_task
def pull_messages():
    """

    This should be scheduled as a periodic task

    """

    for pull_project in PullProject.objects.all():
        # read file into memory?
        # Pull file from FTP

        if not pull_project.pull_from_ftp:
            raise NotImplementedError('PullProject only supports pull_from_ftp')

        if pull_project.from_type != 'CSV':
            raise NotImplementedError('PullProject only supports from_type CSV')

        last_pull, created = LastPull.objects.get_or_create(pull_project=pull_project)

        span = datetime.now() - last_pull.last_pulled
        if span < timedelta(minutes=pull_project.delivery_frequency):
            continue  # not enough time has passed

        session = ftplib.FTP(pull_project.pull_from_ftp.host, pull_project.pull_from_ftp.user, pull_project.pull_from_ftp.password)

        if pull_project.pull_from_ftp.path:
            path = pull_project.pull_from_ftp.path.strip()
            session.cwd(path)

        file_type = '.' + pull_project.from_type.type.lower()
        for file in session.nlst():

            if file.lower().endswith(file_type):
                r = StringIO()
                # session.retrbinary('RETR ' + pull_project.pull_from_ftp.path, r.write)
                session.retrlines('RETR ' + file, lambda line: r.write('%s\n' % line))

                print(r.getvalue())
                original_message = IncomingMessage.objects.create(project=pull_project, message=r.getvalue())
                r.close()

                # convert from CSV to JSON
                if pull_project.to_type.type == 'JSON':
                    outline = pull_project.conversion_parameters
                    csv2json = Csv2Json(outline)
                    converted = csv2json.convert_to_json(original_message.message)
                else:
                    raise NotImplementedError('PullProject only supports the JSON to_type')

                ConvertedMessageQueue.objects.create(original_message=original_message,
                                                     converted_message=converted, project=pull_project)

                if pull_project.pull_from_ftp.processed_path:
                    # Move file to processed folder
                    processed_path = pull_project.pull_from_ftp.processed_path.strip()

                    if processed_path not in session.nlst():
                        session.mkd(processed_path)

                    session.rename(file, processed_path + '/' + file)

        last_pull.save()


def _send_to_api(project, undelivered):
    message_ids = []

    host = project.send_to_api.host

    headers = {'content-type': 'application/json'}

    # //request.add_header('X-Hub-Store', settings.X_Hub_Store)
    # request.add_header('X-Hub-Access-Token', settings.X_Hub_Access_Token)

    for header in project.send_to_api.apiheader_set.all():
        # headers.update({header.name: header.value})
        headers[header.name] = header.value

    for message in undelivered:

        # json.loads(message.converted_message)
        # shipments['shipments'] += json.loads(message.converted_message)
        # message_ids.append(message.id)

        try:
            data = message.converted_message
            response = requests.post(host, data, headers=headers)
            response.raise_for_status()
            message_ids.append(message.id)
            logger.info('Message id %s delivered: %s' % (message.id, response.text))
        except Exception as e:
            logger.error('Error delivering message id %s. Exception Type: %s, Exception: %s' % (message.id, type(e), e))

    return message_ids


def _send_to_ftp(project, undelivered):

    message_ids = []

    file_name = 'workfile-%s.csv' % time.strftime("%Y_%m_%d_%H_%M_%S")
    with open(file_name, 'w') as f:
        for message in undelivered:
            f.write(message.converted_message)
            message_ids.append(message.id)

    # upload file to share
    with open(file_name, 'rb') as upload_file:
        session = ftplib.FTP(project.send_to_ftp.host, project.send_to_ftp.user, project.send_to_ftp.password)
        if project.send_to_ftp.path:
            path = project.send_to_ftp.path.strip()
            project.cwd(path)
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

    for project in Project.objects.all():

        last_delivery, created = LastDelivery.objects.get_or_create(project=project)

        span = datetime.now() - last_delivery.last_delivered
        if span < timedelta(minutes=project.delivery_frequency):
            continue  # not enough time has passed

        undelivered = ConvertedMessageQueue.objects.filter(delivered=False, project=project).order_by('created')

        if not undelivered:
            return

        try:
            if project.send_to_ftp:
                message_ids = _send_to_ftp(project, undelivered)
            else:
                message_ids = _send_to_api(project, undelivered)

            ConvertedMessageQueue.objects.filter(id__in=message_ids).update(delivered=True)
            last_delivery.save()  # update last_delivered time
        except Exception as e:
            logger.error('Error delivering messages for project id %s. Exception Type: %s, Exception: %s' % (project.id, type(e), e))
            if created:
                last_delivery.delete()







