#!/usr/bin/env bash

echo "Waiting for postgres..."

#while ! nc -z $DB_HOST $DB_PORT; do
#  sleep 0.1
#done

sleep 60

echo "PostgreSQL started"

python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput
python3 manage.py migrate sessions
python3 manage.py createsuperuser --no-input || true
python3 manage.py collectstatic --noinput

#python3 manage.py compilemessages -l en -l ru

set -e
chown www-data:www-data /var/log


#uwsgi --strict --ini uwsgi.ini