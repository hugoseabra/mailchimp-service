"""
Tasks to run in parallell
"""

from namespace.models import Namespace
from . import models
from .celery import app
from .service import sync_member as _sync_member


@app.task(bind=True,
          rate_limit='10/m',  # Processar até 10 tasks por minuto
          default_retry_delay=2 * 60,  # retry in 2m
          ignore_result=True)
def sync_all_members(self):
    try:
        for member in models.Member.objects.filter(synchronized=False):
            _sync_member(member)

    except Exception as exc:
        raise self.retry(exc=exc)


@app.task(bind=True,
          rate_limit='10/m',  # Processar até 10 tasks por minuto
          default_retry_delay=2 * 60,  # retry in 2m
          ignore_result=True)
def sync_namespace_members(self, namespace_pk):
    try:
        namespace = Namespace.objects.get(pk=namespace_pk)
        for member in namespace.members.filter(synchronized=False):
            _sync_member(member)

    except Namespace.DoesNotExist as e:
        raise e

    except Exception as exc:
        raise self.retry(exc=exc)


@app.task(bind=True,
          rate_limit='10/m',  # Processar até 10 tasks por minuto
          default_retry_delay=2 * 60,  # retry in 2m
          ignore_result=True)
def sync_member(self, member_pk):
    try:
        member = models.Member.objects.get(pk=member_pk)
        _sync_member(member)

    except models.Member.DoesNotExist as e:
        raise e

    except Exception as exc:
        raise self.retry(exc=exc)
