#!/bin/sh

PG_HOST="localhost"
PG_PORT="5432"

MAX_RETRIES=30
RETRY_INTERVAL=1

i=0
while [ $i -lt $MAX_RETRIES ]; do
    if nc -z -v -w 1 $PG_HOST $PG_PORT 2>/dev/null; then
        echo "PostgreSQL is ready to accept connections"
        exit 0
    else
        i=$((i+1))
        sleep $RETRY_INTERVAL
    fi
done

mkdir -p /usr/src/djelastic/logs
touch /usr/src/djelastic/logs/celery.log
touch /usr/src/djelastic/logs/django.log
chmod -R 777 /usr/src/djelastic/logs
chmod -R 777 /usr/src/djelastic/logs/celery.log
chmod -R 777 /usr/src/djelastic/logs/django.log

# Apply migrations
python manage.py makemigrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
# create admin for testing database
python manage.py create_admin
echo "y" | python manage.py search_index --rebuild
python manage.py create_test_data
python manage.py create_celery_user

exec "$@"
