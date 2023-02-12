#!/bin/bash

# Wait for the database service to be ready
while ! nc -z db 3306; do
  echo "Waiting for database service..."
  sleep 1
done

# Start the Django development server
exec python3 manage.py runserver 0.0.0.0:8000
