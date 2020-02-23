from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class McAudienceConfig(AppConfig):
    name = 'audience'
    verbose_name = _('Audience')

    # noinspection PyUnresolvedReferences
    def ready(self):
        import audience.signals
