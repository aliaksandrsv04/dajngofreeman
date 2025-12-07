from celery import shared_task
import logging
logger = logging.getLogger('api')

@shared_task
def add(x,y):
    print(x,y)
    return x+y

@shared_task(bind=True, max_retries = 5, default_retry_delay = 10)
def scheduled_task(self):
    logger.info("scheduled_task")
    return True