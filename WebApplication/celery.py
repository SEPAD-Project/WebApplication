# myproject/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebApplication.settings')

app = Celery('WebApplication')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()