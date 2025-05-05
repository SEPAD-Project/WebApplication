@echo off
echo Starting Flask app with Waitress...
echo Serving on http://0.0.0.0:2568
waitress-serve --listen=0.0.0.0:2568 wsgi:app
pause
