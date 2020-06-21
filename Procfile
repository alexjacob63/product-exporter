web: gunicorn exporter.wsgi --log-file -
worker: celery worker -A exporter -l info
