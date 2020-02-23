from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class NamespaceConfig(AppConfig):
    name = 'namespace'
    verbose_name = _('Namespace')

    # noinspection PyUnresolvedReferences
    def ready(self):
        import namespace.signals
