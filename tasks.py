import logging
import os
from celery import Celery

app = Celery('worker')
app.conf.update(
    BROKER_URL=os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600},  # 1 hour.
    CELERY_ACCEPT_CONTENT=['json', 'pickle'],
    CELERY_TIMEZONE='US/Eastern',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='pickle'
)

log = logging.getLogger(__name__)


@app.task
def smoke_test():
    log.info("TASK %s", smoke_test.__name__)
    return "ok"
