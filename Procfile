release: python manage.py collectstatic --clear --noinput
web: gunicorn wheels_next_to_sea.wsgi:application