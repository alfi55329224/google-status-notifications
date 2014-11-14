import logging
from datetime import timedelta
import os
from celery import Celery
import feedparser
import requests

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
        send_simple_message()
    else:
        log.info("No entries")


def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v2/sandbox38be6e72fd2d416a900adad83bdf4bda.mailgun.org/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": "Mailgun Sandbox <postmaster@sandbox38be6e72fd2d416a900adad83bdf4bda.mailgun.org>",
              "to": "Damir Suleymanov <gbitle@gmail.com>",
              "subject": "Hello Damir Suleymanov",
              "text": "Google doesn't feel well"})
