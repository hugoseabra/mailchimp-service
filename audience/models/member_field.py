from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import track_data
from core.models.mixins import (
    DeletableModelMixin,
    DateTimeManagementMixin,
    EntityMixin,
    UUIDPkMixin,
)


@track_data('list_field_id', 'member_id', 'reply', )
class MemberField(UUIDPkMixin,
                  EntityMixin,
                  DateTimeManagementMixin,
                  DeletableModelMixin,
                  models.Model):
    """
    Resposta de uma pergunta de uma membro de uma lista
    """

    class Meta:
        verbose_name = _('member field')
        verbose_name_plural = _('member fields')
        unique_together = (
            ('list_field_id', 'member_id'),
        )

    list_field = models.ForeignKey(
        verbose_name=_('list field'),
        to='namespace.ListField',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='member_fields',
    )

    member = models.ForeignKey(
        verbose_name=_('member'),
        to='audience.Member',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='member_fields',
    )

    reply = models.TextField(
        verbose_name=_('reply'),
        null=False,
        blank=False,
    )

    def __repr__(self):
        return '<MemberField member: {}, list_field: {}, pk: {}>'.format(
            self.member_id,
            self.list_field_id,
            self.pk,
        )

    def __str__(self):
        return self.pk

