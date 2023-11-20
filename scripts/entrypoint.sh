#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn app.asgi:application -w 2 -b :8000 -k uvicorn.workers.UvicornWorker
