# from celery import Celery
# from MessageConverter import settings
#
# app = Celery('tasks', backend=settings.CELERY_RESULT_BACKEND, broker=settings.BROKER_URL)
#
# @app.task
# def add(x, y):
#     return x + y

from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    result = x + y

    logger.info('The result: %s' % result)
    return result