from __future__ import absolute_import
import ftplib

from celery import shared_task
from celery.utils.log import get_task_logger

import time
from datetime import datetime, timedelta
from MessageConverter import settings
from message_converter.models import ConvertedMessageQueue, Project, LastDelivery

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
    NotImplementedError('Pull messages task is not currently implemented')

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

        undelivered = ConvertedMessageQueue.objects.filter(delivered=False).order_by('created')

        if not undelivered:
            return

        message_ids = []

        file_name = 'workfile-%s.csv' % time.strftime("%Y_%m_%d_%H_%M_%S")

        if project.send_to_ftp:
            with open(file_name, 'w') as f:
                for message in undelivered:
                    f.write(message.converted_message)
                    message_ids.append(message.id)


            # upload file to share
            with open(file_name, 'rb') as upload_file:
                session = ftplib.FTP(project.send_to_ftp.host, project.send_to_ftp.user, project.send_to_ftp.password)
                session.storlines('STOR ' + file_name, upload_file)
                session.quit()
                ConvertedMessageQueue.objects.filter(id__in=message_ids).update(delivered=True)
        else:
            raise NotImplementedError('Only Send to FTP is currently implemented')





