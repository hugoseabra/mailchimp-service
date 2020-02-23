from django.db.models.signals import post_save
from django.dispatch import receiver

from namespace import models
from namespace.tasks import validate_namespace


@receiver(post_save, sender=models.Namespace)
def validate_namespace_on_save(instance, raw, created, **_):
    """ Validate namespace após criação."""

    if raw is True:
        return

    if created is True:
        validate_namespace(namespace_pk=instance.pk, force_validation=True)
    elif instance.has_changed('default_list_id') is True:
        validate_namespace(namespace_pk=instance.pk, force_validation=False)
