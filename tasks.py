import logging
from datetime import timedelta
import os
from celery import Celery
import feedparser

app = Celery('worker')
app.conf.update(
    BROKER_URL=os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
    CELERY_RESULT_BACKEND=os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'),
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600},  # 1 hour.
    CELERY_ACCEPT_CONTENT=['json', 'pickle'],
    CELERY_TIMEZONE='US/Eastern',
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='pickle',
    CELERYBEAT_SCHEDULE={
        'add-every-30-seconds': {
            'task': 'tasks.check_feed',
            'schedule': timedelta(seconds=30)
        }
    }
)

log = logging.getLogger(__name__)


@app.task
def smoke_test():
    log.info("TASK %s", smoke_test.__name__)
    return "ok"


@app.task(ignore_results=True)
def check_feed():
    d = feedparser.parse('http://www.google.com/appsstatus/rss/en')
    if d.entries:
        for item in d.entries:
            log.info("%s\t%s: %s", item.published, item.title, item.description)
    else:
        log.info("No entries")
