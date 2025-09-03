#!/bin/bash

cd ..

# Create logs directory if it doesn't exist
mkdir -p logs

# Generate timestamp for log files
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

source .venv/bin/activate

echo "Starting Django server..."
python3 manage.py runserver 0.0.0.0:8000 > "logs/django_$TIMESTAMP.log" 2>&1 &

# Save PID to file
echo $! > logs/django.pid

sleep 2

echo "Starting Celery worker..."
celery -A WebApplication worker --loglevel=info > "logs/celery_$TIMESTAMP.log" 2>&1 &

# Save PID to file
echo $! > logs/celery.pid

echo "Services started successfully!"
echo "Django PID: $(cat logs/django.pid)"
echo "Celery PID: $(cat logs/celery.pid)"
echo "Logs: logs/django_$TIMESTAMP.log"
echo "Logs: logs/celery_$TIMESTAMP.log"