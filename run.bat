::Use this for production server. for development server use run.py
@echo off
echo Use this for production server. for development server use run.py
echo Fetch changes from github and clean repository
git fetch --all
git reset --hard origin/main
git clean -fd 
echo Starting Celery service...
celery -A source.celery worker --loglevel=info -P threads
echo Starting Flask app with Waitress...
echo Serving on http://0.0.0.0:2568
waitress-serve --listen=0.0.0.0:2568 source.app:app
pause
