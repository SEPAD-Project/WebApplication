#Use this for development server. for production server use run.bat
from source.app import app
import subprocess

if __name__=='__main__':
    print('Use this for development server. for production server use run.bat')

    print('Starting Celery service..')
    subprocess.Popen([
        "celery", 
        "-A", "source.celery", 
        "worker", 
        "--loglevel=info", 
        "-P", "threads"
    ])
    
    print('Starting Flask app with flask run tool...')
    app.run(host='0.0.0.0', port='2568', debug=True)