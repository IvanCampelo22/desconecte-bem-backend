from __future__ import absolute_import, unicode_literals
from base_tasks.schedule import CELERY_BEAT_SCHEDULE
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'descbem.settings')

app = Celery('descbem') 

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = CELERY_BEAT_SCHEDULE

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")