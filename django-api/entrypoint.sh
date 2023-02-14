#!/bin/bash

# Set the host based on the value of ENV
if [ "$ENV" == "dev" ]; then
  HOST="bd"
elif [ "$ENV" == "prod" ]; then
  HOST="gtd-mysql-1.cghnoav6qten.us-east-1.rds.amazonaws.com"
else
  echo "Invalid value for ENV: $ENV"
  exit 1
fi

# Wait for the database service to be ready
while ! nc -z "$HOST" 3306; do
  echo "Waiting for database service..."
  sleep 1
done

# Start the Django development server
exec python3 manage.py runserver "$HOST:8000"
