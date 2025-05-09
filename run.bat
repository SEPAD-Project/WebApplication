@echo off
echo fetch codes from github and get the latest version
git fetch --all
git reset --hard origin/main
git clean -fd
echo Starting Flask app with Waitress...
echo Serving on http://0.0.0.0:2568
waitress-serve --listen=0.0.0.0:2568 source.wsgi:app
pause
