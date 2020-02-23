"""
Tasks to run in parallell
"""

from . import models
from .celery import app
from .service import validate_namespace as _validate_namespace


@app.task(bind=True,
          rate_limit='10/m',  # Processar até 10 tasks por minuto
          default_retry_delay=2 * 60,  # retry in 2m
          ignore_result=True)
def validate_namespaces(self, force_validation=False):
    try:
        for n in models.Namespace.objects.all():
            _validate_namespace(n, force_validation)

    except Exception as exc:
        raise self.retry(exc=exc)


@app.task(bind=True,
          rate_limit='10/m',  # Processar até 10 tasks por minuto
          default_retry_delay=2 * 60,  # retry in 2m
          ignore_result=True)
def validate_namespace(self, namespace_pk, force_validation=False):
    try:
        namespace = models.Namespace.objects.get(pk=namespace_pk)
        _validate_namespace(namespace, force_validation)

    except models.Namespace.DoesNotExist as e:
        raise e

    except Exception as exc:
        raise self.retry(exc=exc)
