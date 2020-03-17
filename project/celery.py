from celery import Celery
from kombu import Queue, Exchange

app = Celery('mailchimp')
app.config_from_object('django.conf:settings', namespace='CELERY')

app_names = (
    'namespace',
    'audience',
)

queues = list()

for app_name in app_names:
    queues.append(Queue(
        name=app_name,
        exchange=Exchange(name='mailchimp', type='direct', delivery_mode=2),
        routing_key=app_name,
        durable=True,
    ))

app.conf.task_queues = queues

app.autodiscover_tasks()
