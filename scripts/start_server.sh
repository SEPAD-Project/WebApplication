#!/bin/bash
set -e

# ==========================
# Configuration
# ==========================
DJANGO_PORT=8000
LOG_DIR=logs
VENV_PATH=.venv/bin/activate
CELERY_APP=WebApplication

# ==========================
# Go up one directory
# ==========================
cd ..

# ==========================
# Create logs directory
# ==========================
mkdir -p "$LOG_DIR"

# ==========================
# Generate timestamp
# ==========================
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# ==========================
# Activate virtual environment
# ==========================
if [ -f "$VENV_PATH" ]; then
    echo "Activating virtual environment..."
    source "$VENV_PATH"
else
    echo "Virtual environment not found at '$VENV_PATH'."
    exit 1
fi

# ==========================
# Start Django server
# ==========================
echo "Starting Django server on port $DJANGO_PORT..."
python3 manage.py runserver 0.0.0.0:$DJANGO_PORT > "$LOG_DIR/django_$TIMESTAMP.log" 2>&1 &
DJANGO_PID=$!
echo $DJANGO_PID > "$LOG_DIR/django.pid"

# ==========================
# Wait a little before starting Celery
# ==========================
sleep 2

# ==========================
# Start Celery worker
# ==========================
echo "Starting Celery worker..."
celery -A $CELERY_APP worker --loglevel=info > "$LOG_DIR/celery_$TIMESTAMP.log" 2>&1 &
CELERY_PID=$!
echo $CELERY_PID > "$LOG_DIR/celery.pid"

# ==========================
# Summary
# ==========================
echo
echo "========================================"
echo "Services started successfully!"
echo "Django PID: $DJANGO_PID"
echo "Celery PID: $CELERY_PID"
echo "Django log: $LOG_DIR/django_$TIMESTAMP.log"
echo "Celery log: $LOG_DIR/celery_$TIMESTAMP.log"
echo "The window will close in 5 seconds..."
echo "========================================"

sleep 5
