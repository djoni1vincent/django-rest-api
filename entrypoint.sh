#!/bin/bash

echo "Running migrations..."
uv run python manage.py migrate

echo "Ensuring superuser exists..."
uv run python manage.py createsuperuser --noinput || true

echo "Collecting static files..."
uv run python manage.py collectstatic --noinput

echo "Starting server..."
uv run gunicorn config.wsgi --bind 0.0.0.0:8000
