@echo off
setlocal enabledelayedexpansion

cd ..

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Get current timestamp for log files
for /f "tokens=2 delims=." %%a in ('echo %time%') do set timestamp=%%a
set timestamp=%date:~-4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%

REM Function to check if port is available
:check_port
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
    echo Port 8000 is occupied by PID %%a
    taskkill /PID %%a /F >nul 2>&1
    timeout /t 1 >nul
    goto check_port
)

REM Start Django development server with logging
echo Starting Django development server...
start "Django Server" cmd /c "python manage.py runserver 0.0.0.0:8000 > logs\django_%timestamp%.log 2>&1 & echo Django server started on port 8000 & pause"

REM Wait for Django to start
echo Waiting for Django to start...
timeout /t 5 >nul

REM Check if Django started successfully
tasklist /fi "windowtitle eq Django Server" | find /i "cmd.exe" >nul
if errorlevel 1 (
    echo ERROR: Django server failed to start!
    goto error
)

REM Start Celery worker with logging
echo Starting Celery worker...
start "Celery Worker" cmd /c "celery -A WebApplication worker --pool=solo --loglevel=info > logs\celery_%timestamp%.log 2>&1 & echo Celery worker started & pause"

REM Wait for Celery to start
echo Waiting for Celery to start...
timeout /t 3 >nul

REM Check if Celery started successfully
tasklist /fi "windowtitle eq Celery Worker" | find /i "cmd.exe" >nul
if errorlevel 1 (
    echo ERROR: Celery worker failed to start!
    goto error
)

REM Save PIDs to files for easy stopping
for /f "tokens=2" %%a in ('tasklist /fi "windowtitle eq Django Server" /fo csv /nh') do (
    set django_pid=%%~a
    echo !django_pid! > logs\django_pid.txt
)

for /f "tokens=2" %%a in ('tasklist /fi "windowtitle eq Celery Worker" /fo csv /nh') do (
    set celery_pid=%%~a
    echo !celery_pid! > logs\celery_pid.txt
)

echo.
echo ========================================
echo Services started successfully!
echo ========================================
echo Django Server: http://0.0.0.0:8000
echo Django PID: !django_pid!
echo Celery PID: !celery_pid!
echo Logs: logs\django_%timestamp%.log
echo Logs: logs\celery_%timestamp%.log
echo.
echo Use 'stop_server.bat' to stop both services
echo ========================================
goto end

:error
echo.
echo ========================================
echo Failed to start services!
echo Check the log files in the logs directory
echo ========================================
pause
exit /b 1

:end
endlocal