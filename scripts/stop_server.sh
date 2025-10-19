#!/bin/bash
set -e

LOG_DIR=logs
CELERY_APP=WebApplication

echo "Stopping services..."

# ==========================
# Stop Django using PID file
# ==========================
if [ -f "$LOG_DIR/django.pid" ]; then
    DJANGO_PID=$(cat "$LOG_DIR/django.pid")
    echo "Stopping Django server (PID: $DJANGO_PID)..."
    kill "$DJANGO_PID" 2>/dev/null || true
    rm "$LOG_DIR/django.pid"
fi

# ==========================
# Stop Celery using PID file
# ==========================
if [ -f "$LOG_DIR/celery.pid" ]; then
    CELERY_PID=$(cat "$LOG_DIR/celery.pid")
    echo "Stopping Celery worker (PID: $CELERY_PID)..."
    kill "$CELERY_PID" 2>/dev/null || true
    rm "$LOG_DIR/celery.pid"
fi

# ==========================
# Force kill any remaining processes (fallback)
# ==========================
echo "Cleaning up any remaining processes..."
pkill -f "manage.py runserver" 2>/dev/null || true
pkill -f "celery -A $CELERY_APP" 2>/dev/null || true

sleep 1

echo "All services stopped successfully!"
echo "The window will close in 5 seconds..."
sleep 5
