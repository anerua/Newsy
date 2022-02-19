release: python manage.py migrate
web: gunicorn newsy.wsgi --log-file -
# main_worker: python manage.py celery worker --beat --loglevel=info
# worker: celery -A newsyapp.celery worker -l info -B
# worker: celery -A newsyapp.celery worker -B -l --loglevel=info
worker: celery -A newsyapp.celery worker --beat --loglevel=info 