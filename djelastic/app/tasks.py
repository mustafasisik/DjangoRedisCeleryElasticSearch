from celery import shared_task
import logging
from django.conf import settings


logger_debug = logging.getLogger('celery_debug')


@shared_task(bind=True)
def log_search(self, *args, **kwargs):

    print(kwargs)
    try:
        key = kwargs["key"]
        value = kwargs["value"]
        username = kwargs["username"]
        logger_debug.debug(f"User {username} searched for: key:{key} and value:{value}")
        return
    except Exception as e:
        logger_debug.debug(f"Error {e}")
        return