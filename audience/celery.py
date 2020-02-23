import logging
import os

from celery import Celery
from django.conf import settings
from kombu import Queue, Exchange

CELERY_QUEUES = (
    Queue(
        'celery',
        Exchange('transient', delivery_mode=2),
        routing_key='celery',
        durable=True,
    ),
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

logger = logging.getLogger("Celery[Audience]")
app = Celery('namespace')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
