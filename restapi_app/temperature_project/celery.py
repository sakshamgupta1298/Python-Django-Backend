# celery.py

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'temperature_project.settings')

# Create a Celery instance
app = Celery('temperature_project')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all apps in your Django project
app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
