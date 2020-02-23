from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MailchimpServiceConfig(AppConfig):
    name = 'mailchimp_service'
    verbose_name = _('MailChimp Service')
