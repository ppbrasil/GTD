#!/bin/bash

# Set the host based on the value of ENV
echo "env is: $ENV"
if [ "$ENV" == "dev" ]; then
  HOST="db"
elif [ "$ENV" == "prod" ]; then
  HOST="gtd-mysql-1.cghnoav6qten.us-east-1.rds.amazonaws.com"
else
  echo "Invalid value for ENV: $ENV"
  exit 1
fi

# Wait for the database service to be ready
while ! nc -z "$HOST" 3306; do
  echo "Waiting for database service on $HOST 3306..."
  sleep 1
done

# Start the Django development server
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py migrate test
service cron start
python3 manage.py runserver 0.0.0.0:8000
