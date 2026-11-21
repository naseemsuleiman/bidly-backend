#!/bin/sh
set -e

echo "Running migrations…"
python manage.py migrate --noinput

echo "Collecting static…"
python manage.py collectstatic --noinput

echo "Starting server…"
exec gunicorn config.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 60