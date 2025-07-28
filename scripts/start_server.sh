#!/bin/bash

cd ..

source .venv/bin/activate

echo "🟢 Starting Django server..."
python3 manage.py runserver 0.0.0.0:8000&

sleep 2

echo "🔄 Starting Celery worker..."
celery -A WebApplication worker --loglevel=info
