web: gunicorn main:app --log-file -
worker: celery worker -A tasks --loglevel INFO --concurrency=1
beat: celery beat -A tasks --loglevel INFO
