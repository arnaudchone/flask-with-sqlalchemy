release: python manage.py db upgrade
web: gunicorn wsgi:app --access-logfile=-
celery -A tasks.celery worker --loglevel=info
