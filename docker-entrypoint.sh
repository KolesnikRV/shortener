#!/bin/bash
# Create database migrations
echo "Creating database migrations"
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Start server + celery
echo "Starting server + celery"
python manage.py runserver 0.0.0.0:8000 & celery -A shortener worker -B
