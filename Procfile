release: python manage.py migrate
web: gunicorn newsy.wsgi --log-file -
main_worker: python manage.py celery worker --beat --loglevel=info
# worker: celery -A newsy worker -l info -B