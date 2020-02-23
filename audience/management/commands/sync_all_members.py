from django.core.management.base import BaseCommand

from audience.tasks import sync_member
from namespace.management.commands.namespace_command_mixin import \
    NamespaceCommandCommandMixin
from namespace.models import Namespace


class Command(NamespaceCommandCommandMixin, BaseCommand):
    help = "Synchronizes all members."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.process_options(options)

        for namespace in Namespace.objects.all():
            if self.interactive:
                self.stdout.write(
                    '  - {} ({}): '.format(namespace, namespace.pk)
                )

            for m in namespace.members.filter(synchronized=False):
                self.stdout.write(
                    '      - {} ({}): '.format(m.full_name, m.pk),
                    ending='',
                )

                sync_member(m.pk)

                if self.interactive:
                    self.stdout.write(self.style.SUCCESS('OK'))
                    self.stdout.write("\n")
