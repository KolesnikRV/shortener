from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shortener.settings')

app = Celery('shortener')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_data_on_shedule': {
        'task': 'url.tasks.delete_old_data_db',
        'schedule': settings.CLEAR_DATA_MINUTES * 60,
    },
}

app.conf.timezone = 'UTC'
