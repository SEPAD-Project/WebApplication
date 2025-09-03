#!/bin/bash
echo "Stopping services..."

# Stop Django using PID file
if [ -f logs/django.pid ]; then
    echo "Stopping Django server (PID: $(cat logs/django.pid))..."
    kill $(cat logs/django.pid) 2>/dev/null
    rm logs/django.pid
fi

# Stop Celery using PID file
if [ -f logs/celery.pid ]; then
    echo "Stopping Celery worker (PID: $(cat logs/celery.pid))..."
    kill $(cat logs/celery.pid) 2>/dev/null
    rm logs/celery.pid
fi

# Force kill any remaining processes (fallback)
echo "Cleaning up any remaining processes..."
pkill -f "manage.py runserver" 2>/dev/null
pkill -f "celery -A WebApplication" 2>/dev/null

sleep 1

echo "All services stopped successfully!"