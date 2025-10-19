@echo off
setlocal

REM ==========================
REM Configuration
REM ==========================
set DJANGO_PORT=8000
set VENV_PATH=.venv\Scripts\activate.bat
set DJANGO_CMD=python manage.py runserver 0.0.0.0:%DJANGO_PORT%
set CELERY_CMD=celery -A WebApplication worker --pool=solo --loglevel=info

REM ==========================
REM Go up one directory
REM ==========================
echo Changing directory to project root...
cd ..

REM ==========================
REM Activate virtual environment
REM ==========================
if exist "%VENV_PATH%" (
    echo Activating virtual environment...
    call "%VENV_PATH%"
) else (
    echo Virtual environment not found at "%VENV_PATH%".
    goto :end
)

REM ==========================
REM Free the port if occupied
REM ==========================
echo Checking if port %DJANGO_PORT% is in use...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":%DJANGO_PORT%"') do (
    echo Port %DJANGO_PORT% is occupied by PID %%a. Terminating process...
    taskkill /PID %%a /F >nul 2>&1
)

REM ==========================
REM Start Django server
REM ==========================
echo Starting Django server on port %DJANGO_PORT%...
start "Django Server" cmd /c "%DJANGO_CMD%"

REM ==========================
REM Start Celery worker
REM ==========================
echo Starting Celery worker...
start "Celery Worker" cmd /c "%CELERY_CMD%"

echo.
echo ========================================
echo All services started successfully!
echo Django Server: http://0.0.0.0:%DJANGO_PORT%
echo Close the windows or use the stop script to terminate services.
echo ========================================

REM ==========================
REM Wait a few seconds before closing this window
REM ==========================
echo The window will automatically close in 5 seconds.
timeout /t 5 /nobreak >nul

:end
endlocal
exit
