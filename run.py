import subprocess
import os
from source.app import app

def kill_existing_celery():
    print('Checking for existing Celery worker...')
    check = subprocess.run(
        'tasklist | findstr celery.exe',
        shell=True,
        capture_output=True,
        text=True
    )

    if "celery.exe" in check.stdout.lower():
        print("Found Celery process. Killing...")
        subprocess.call(
            'taskkill /IM celery.exe /F >nul 2>&1',
            shell=True
        )
        print("Celery process killed successfully.")
    else:
        print("No Celery process found to kill.")

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        kill_existing_celery()

        print('Starting Celery worker in new window...')

        command = (
            '.venv\\Scripts\\activate && '
            'python -m celery -A source.celery worker --loglevel=info -P threads'
        )

        subprocess.Popen(
            f'start "CeleryWorker" cmd /k "{command}"',
            shell=True
        )

    print('Starting Flask app...')
    app.run(host='0.0.0.0', port=2568, debug=True)
