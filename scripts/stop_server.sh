#!/bin/bash
echo "⛔ Stopping Django runserver..."
pkill -f "manage.py runserver"

echo "⛔ Stopping Celery worker..."
pkill -f "celery -A"
