from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import track_data
from core.models.mixins import (
    DateTimeManagementMixin,
    DeletableModelMixin,
    EntityMixin,
    UUIDPkMixin,
)


@track_data('namespace_id', 'label', 'tag')
class ListField(UUIDPkMixin,
                EntityMixin,
                DeletableModelMixin,
                DateTimeManagementMixin,
                models.Model):
    """
    Campo adicionado a uma lista.
    """

    class Meta:
        verbose_name = _('list field')
        verbose_name_plural = _('list fields')
        unique_together = (
            ('namespace_id', 'tag',),
        )

    FIELD_TYPE_TEXT = 'text'
    FIELD_TYPE_NUMBER = 'number'

    FIELD_TYPES = (
        (FIELD_TYPE_TEXT, _('Text')),
        (FIELD_TYPE_NUMBER, _('Number')),
    )

    namespace = models.ForeignKey(
        verbose_name=_('namespace'),
        to='namespace.Namespace',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='fields',
    )

    field_type = models.CharField(
        max_length=6,
        verbose_name=_('field type'),
        null=False,
        blank=False,
        choices=FIELD_TYPES,
        default=FIELD_TYPE_TEXT,
    )

    label = models.CharField(
        max_length=50,
        verbose_name=_('label'),
        null=False,
        blank=False,
    )

    tag = models.CharField(
        max_length=50,
        verbose_name=_('tag'),
        null=False,
        blank=False,
    )

    help_text = models.CharField(
        max_length=255,
        verbose_name=_('help text'),
        null=True,
        blank=True,
    )

    active = models.BooleanField(
        verbose_name=_('active'),
        default=False,
        null=False,
        blank=False,
        help_text=_('If true, it means that the field will be created in list'
                    ' in MailChimp platform.'),
    )

    def to_sync_data(self):
        return {
            'name': self.label,
            'tag': self.tag,
            'type': self.field_type,
            'required': False,
            'list_id': self.namespace.default_list_id,
            'help_text': self.help_text,
        }

    def __repr__(self):
        return '<ListField pk: {}, label: {}, tag: {}'.format(
            self.pk,
            self.label,
            self.tag,
        )

    def __str__(self):
        return '{} ({})'.format(self.label, self.tag)
