from django.db.models.signals import post_save
from django.dispatch import receiver

from audience import models


@receiver(post_save, sender=models.Member)
def update_synchronization_type_on_edition(instance, raw, created, **_):
    """ Atualiza tipo de sincronização após criação ou edição."""

    if raw is True:
        return

    has_changed = instance.has_changed('namespace_id') or \
                  instance.has_changed('first_name') or \
                  instance.has_changed('last_name') or \
                  instance.has_changed('email')

    miss_mc_id = not instance.mailchimp_id

    schedule_to_sync = created or miss_mc_id or has_changed

    if schedule_to_sync is True:
        models.Member.objects.filter(pk=instance.pk).update(**{
            'synchronized': False,
        })
