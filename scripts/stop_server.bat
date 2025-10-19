@echo off
setlocal

echo Stopping Django and Celery processes...

for /f "tokens=2 delims=," %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH') do (
    tasklist /FI "PID eq %%~a" /FO LIST | findstr /I "manage.py celery" >nul
    if %ERRORLEVEL%==0 (
        echo Killing process PID %%a...
        taskkill /PID %%a /F >nul 2>&1
    )
)

echo All Django and Celery processes have been terminated.

REM Wait a few seconds so the user can read the message
echo The window will automatically close in 5 seconds.
timeout /t 5 /nobreak >nul

endlocal
exit
