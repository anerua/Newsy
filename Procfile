release: python manage.py migrate
web: gunicorn newsy.wsgi --log-file -
worker: celery -A newsyapp.celery worker --beat --loglevel=info 