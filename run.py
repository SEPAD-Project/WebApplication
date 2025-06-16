import subprocess
import os
import time
from source.app import app

def print_section(title):
    print()
    print("=" * 60)
    print(title)
    print("-" * 60)

def kill_celery_process():
    print_section("Stopping any existing Celery processes")

    # Small delay to ensure previous processes are fully initialized
    time.sleep(1)

    # Terminate cmd.exe processes running celery
    subprocess.run(
        'wmic process where "CommandLine like \'%celery%\' and name=\'cmd.exe\'" call terminate',
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    )

    # Terminate python.exe processes running celery
    subprocess.run(
        'wmic process where "CommandLine like \'%celery%\' and name=\'python.exe\'" call terminate',
        shell=True,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL
    )

    print("Celery processes shutdown complete.")
    time.sleep(1)

def start_celery_worker():
    print_section("Starting new Celery worker")

    bat_path = os.path.abspath("celery_worker.bat")
    if not os.path.exists(bat_path):
        print(f"ERROR: celery_worker.bat not found at: {bat_path}")
        return

    subprocess.Popen(
        f'start "CeleryWorker" cmd /k "{bat_path}"',
        shell=True
    )

    print("New Celery worker launched.")

if __name__ == '__main__':
    # Kill processes immediately on startup (first run of reloader)
    kill_celery_process()

    # Start celery only in the main reloader process
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        start_celery_worker()

    print_section("Starting Flask server")
    app.run(host='0.0.0.0', port=85, debug=True)
