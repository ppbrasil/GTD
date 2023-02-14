#!/bin/bash

# Wait for the database service to be ready
while ! nc -z gtd-mysql-1.cghnoav6qten.us-east-1.rds.amazonaws.com 3306; do
  echo "Waiting for database service on gtd-mysql-1.cghnoav6qten.us-east-1.rds.amazonaws.com 3306..."
  sleep 1
done

# Start the Django development server
exec python3 manage.py runserver
