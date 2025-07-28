@echo off

cd ..

REM
call .venv\Scripts\activate.bat

REM
echo Starting Django development server...
start cmd /k "python manage.py runserver 0.0.0.0:8000"

REM
timeout /t 2 >nul

REM
echo Starting Celery worker...
start cmd /k "celery -A WebApplication worker --loglevel=info"
