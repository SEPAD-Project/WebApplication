@echo off
setlocal enabledelayedexpansion

echo Stopping Django runserver...
for /f "tokens=2,3 delims=," %%a in ('wmic process where "CommandLine like '%%manage.py%%'" get ProcessId^,ParentProcessId /format:csv ^| findstr /i "manage.py"') do (
    echo Terminating PID %%a and parent CMD %%b
    taskkill /PID %%a /F >nul
    taskkill /PID %%b /F >nul
)

echo Stopping Celery worker...
for /f "tokens=2,3 delims=," %%a in ('wmic process where "CommandLine like '%%celery%%'" get ProcessId^,ParentProcessId /format:csv ^| findstr /i "celery"') do (
    echo Terminating PID %%a and parent CMD %%b
    taskkill /PID %%a /F >nul
    taskkill /PID %%b /F >nul
)
