:: Use this for production server. For development use run.py
@echo off
echo Use this for production server. For development use run.py

echo Fetching changes from GitHub and cleaning repository...
git fetch --all
git reset --hard origin/main
git clean -fd 

echo Starting Celery worker in a new window...
start "Celery Worker" cmd /k ".venv\Scripts\activate && python -m celery -A source.celery worker --loglevel=info -P threads"

echo Starting Flask app with Waitress in new window...
start "Flask Server" cmd /k ".venv\Scripts\activate && waitress-serve --listen=0.0.0.0:2568 source.app:app"

