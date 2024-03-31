#!/usr/bin/env bash

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py migrate sessions
python3 manage.py createsuperuser --username root --email email@email.com --no-input || true
python3 manage.py collectstatic --noinput

#python3 manage.py compilemessages -l en -l ru

set -e
chown www-data:www-data /var/log


uwsgi --strict --ini uwsgi/uwsgi.ini