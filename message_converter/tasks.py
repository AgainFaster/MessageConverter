from __future__ import absolute_import
import ftplib

from celery import shared_task
from celery.utils.log import get_task_logger

import time
from MessageConverter import settings
from message_converter.models import ConvertedMessageQueue

logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    result = x + y

    logger.info('The result: %s' % result)
    return result

@shared_task
def deliver_messages():
    undelivered = ConvertedMessageQueue.objects.filter(delivered=False).order_by('created')

    if not undelivered:
        return

    message_ids = []

    file_name = 'workfile-%s.csv' % time.strftime("%Y_%m_%d_%H_%M_%S")
    with open(file_name, 'w') as f:
        for message in undelivered:
            f.write(message.converted_message)
            message_ids.append(message.id)


    # upload file to share
    with open(file_name, 'rb') as upload_file:
        session = ftplib.FTP(getattr(settings, 'FTP_HOST', None),
                             getattr(settings, 'FTP_USER', None),
                             getattr(settings, 'FTP_PASSWD', None),)
        session.storlines('STOR ' + file_name, upload_file)
        session.quit()

    ConvertedMessageQueue.objects.filter(id__in=message_ids).update(delivered=True)


