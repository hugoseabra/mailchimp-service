from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import track_data
from core.models.mixins import (
    DateTimeManagementMixin,
    DeletableModelMixin,
    EntityMixin,
    UUIDPkMixin,
)
from mailchimp_service import service


@track_data('default_list_id')
class Namespace(UUIDPkMixin,
                EntityMixin,
                DeletableModelMixin,
                DateTimeManagementMixin,
                models.Model):
    """
    Namespace de uma aplicação cliente que consome o service de integração
    com Mail Chimp e carrega informações referentes à conta do MailChimp
    a ser conectada.
    """

    class Meta:
        verbose_name = _('namespace')
        verbose_name_plural = _('namespaces')
        unique_together = (
            ('external_id', 'slug',),
        )

    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
        null=False,
        blank=False,
    )

    slug = models.SlugField(
        max_length=255,
        verbose_name=_('slug'),
        null=False,
        blank=False,
    )

    default_tag = models.CharField(
        max_length=80,
        verbose_name=_('Default tag'),
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )

    external_id = models.CharField(
        max_length=255,
        verbose_name=_('external ID'),
        null=False,
        blank=False,
        unique=True,
        db_index=True,
    )

    api_key = models.CharField(
        max_length=48,
        verbose_name=_('api key'),
        null=False,
        blank=False,
        db_index=True,
    )

    default_list_id = models.CharField(
        max_length=20,
        verbose_name=_('default list ID'),
        null=True,
        blank=True,
    )

    default_list_name = models.CharField(
        max_length=255,
        verbose_name=_('default list name'),
        null=True,
        blank=True,
        editable=False,
    )

    healthy = models.BooleanField(
        verbose_name=_('healthy'),
        default=False,
        null=False,
        blank=False,
        help_text=_('If false, it means that mailchimp api key or list ID are'
                    ' not available.'),
    )

    sync_address = models.BooleanField(
        verbose_name=_('synchronize address'),
        default=False,
        null=False,
        blank=False,
        help_text=_('If true, the service will send member address to'
                    ' mailchimp.'),
    )

    sync_phone = models.BooleanField(
        verbose_name=_('synchronize phone'),
        default=False,
        null=False,
        blank=False,
        help_text=_('If true, the service will send member phone to'
                    ' mailchimp.'),
    )

    create_fields = models.BooleanField(
        verbose_name=_('synchronize fields'),
        default=False,
        null=False,
        blank=False,
        help_text=_('If true, the service will create and register value in'
                    ' custom fields in member record in mailchimp.'),
    )

    create_notes = models.BooleanField(
        verbose_name=_('create notes'),
        default=False,
        null=False,
        blank=False,
        help_text=_('If true, the service will create notes in member record'
                    ' in mailchimp.'),
    )

    @property
    def service(self):
        return service.get_client(namespace_name=self.name,
                                  api_key=self.api_key)

    def __repr__(self):
        return '<Namespace pk: {}, name: {}, external_id: {}'.format(
            self.pk,
            self.name,
            self.external_id,
        )

    def __str__(self):
        if self.default_list_name:
            list_name = ' - {}'.format(self.default_list_name)
        else:
            list_name = ''

        return '{}{}'.format(self.name, list_name)
