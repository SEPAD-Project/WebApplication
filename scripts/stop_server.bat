@echo off
echo Stopping services...

REM Stop processes by window title (most reliable method)
echo Stopping Django server...
taskkill /fi "windowtitle eq Django Server" /f >nul 2>&1

echo Stopping Celery worker...
taskkill /fi "windowtitle eq Celery Worker" /f >nul 2>&1

REM Additional cleanup - kill Python processes that might be orphaned
echo Cleaning up Python processes...
timeout /t 1 >nul
taskkill /im python.exe /f >nul 2>&1

REM Clean up PID files if they exist
if exist logs\django_pid.txt del logs\django_pid.txt >nul 2>&1
if exist logs\celery_pid.txt del logs\celery_pid.txt >nul 2>&1

echo All services stopped successfully!
pause