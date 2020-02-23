from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import track_data
from core.models.mixins import (
    DeletableModelMixin,
    DateTimeManagementMixin,
    EntityMixin,
    UUIDPkMixin,
)


@track_data('namespace_id', 'first_name', 'last_name', 'email',)
class Member(UUIDPkMixin,
             EntityMixin,
             DateTimeManagementMixin,
             DeletableModelMixin,
             models.Model):
    """
    Membro de uma Lista de Audiência
    """

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')
        unique_together = (
            ('namespace_id', 'external_id'),
            ('namespace_id', 'mailchimp_id'),
        )

    namespace = models.ForeignKey(
        verbose_name=_('namespace'),
        to='namespace.Namespace',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        related_name='members',
    )

    first_name = models.CharField(
        max_length=100,
        verbose_name=_('first name'),
        null=False,
        blank=False,
    )

    last_name = models.CharField(
        max_length=100,
        verbose_name=_('last name'),
        null=False,
        blank=False,
    )

    email = models.EmailField(
        max_length=255,
        verbose_name=_('e-mail'),
        null=False,
        blank=False,
    )

    birthday = models.DateField(
        verbose_name=_('birthday'),
        null=True,
        blank=True,
    )

    phone_country_code = models.CharField(
        max_length=5,
        verbose_name=_('DDI'),
        null=True,
        blank=True,
    )

    phone_region_code = models.CharField(
        max_length=5,
        verbose_name=_('DDD'),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
        verbose_name=_('phone number'),
        null=True,
        blank=True,
    )

    address1 = models.TextField(
        verbose_name=_('address 1'),
        null=True,
        blank=True,
    )

    address2 = models.TextField(
        verbose_name=_('address 2'),
        null=True,
        blank=True,
    )

    city = models.CharField(
        max_length=150,
        verbose_name=_('city'),
        null=True,
        blank=True,
    )

    state = models.CharField(
        max_length=80,
        verbose_name=_('state'),
        null=True,
        blank=True,
    )

    zip_code = models.CharField(
        max_length=80,
        verbose_name=_('zip code'),
        null=True,
        blank=True,
    )

    external_id = models.TextField(
        verbose_name=_('external ID'),
        null=False,
        blank=False,
    )

    mailchimp_id = models.TextField(
        verbose_name=_('mailchimp ID'),
        null=True,
        blank=True,
        editable=False,
    )

    tags = models.TextField(
        verbose_name=_('tags'),
        null=True,
        blank=True,
    )

    synchronized = models.BooleanField(
        verbose_name=_('synchronized'),
        default=False,
        null=False,
        blank=False,
        help_text=_('If true, it means that the member has been saved / edited'
                    ' in MailChimp platform.'),
    )

    excluded = models.BooleanField(
        verbose_name=_('excluded'),
        default=False,
        null=False,
        blank=False,
        help_text=_('If true, the member will be scheduled to unsubscribe'
                    ' in mailchimp and then be deleted.'),
    )

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def phone(self):
        return '+{}{}{}'.format(
            self.phone_country_code.lstrip('+'),
            self.phone_region_code,
            self.phone_number,
        )

    @property
    def healthy(self):
        return self.namespace.healthy is True

    @property
    def sync_create(self):
        return self.excluded is False and not self.mailchimp_id

    @property
    def sync_update(self):
        return self.excluded is False and (not self.mailchimp_id) is False

    @property
    def sync_delete(self):
        return self.excluded is True

    def __repr__(self):
        return '<Member name: {}, pk: {}, external_id:{}>'.format(
            self.full_name,
            self.pk,
            self.external_id,
        )

    def __str__(self):
        return '{} - {}'.format(self.full_name, self.external_id)

    def to_sync_data(self):
        fields = dict()

        fields['FNAME'] = self.first_name
        fields['LNAME'] = self.last_name

        if self.namespace.sync_address is True:
            address = dict()

            if self.address1:
                address['addr1'] = self.address1

            if self.address2:
                address['addr2'] = self.address2

            if self.city:
                address['city'] = self.city

            if self.state:
                address['state'] = self.state

            if self.zip_code:
                address['zip'] = self.zip_code

            if address:
                address['country'] = 'BR'
                fields['ADDRESS'] = address

        if self.phone_number and self.namespace.sync_phone is True:
            fields['PHONE'] = self.phone

        if self.birthday:
            fields['BIRTHDAY'] = self.birthday.strftime('%m/%d')

        if self.namespace.create_fields:
            for member_f in self.member_fields.all():
                fields[member_f.list_field.tag] = member_f.reply

        data = {
            'list_id': self.namespace.default_list_id,
            'email_address': self.email,
            'email_type': 'html',
            'language': 'pt',
            'merge_fields': fields,
        }

        if self.mailchimp_id:
            data.update({
                'id': self.mailchimp_id,
            })

        return data
