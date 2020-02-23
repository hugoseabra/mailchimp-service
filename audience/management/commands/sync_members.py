from django.core.management import call_command
from django.core.management.base import BaseCommand

from namespace.management.commands.namespace_command_mixin import \
    NamespaceCommandCommandMixin
from namespace.models import Namespace


class Command(NamespaceCommandCommandMixin, BaseCommand):
    help = "Synchronizes members of a namespace which are not already" \
           " synchronized according to sychronization types."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.process_options(options)

        for namespace in Namespace.objects.all():
            if self.interactive:
                self.stdout.write(
                    '  - {} ({}): '.format(
                        namespace,
                        namespace.pk,
                    ),
                    ending='',
                )

            call_args = [
                'sync_member',
                namespace.api_key,
                namespace.external_id,
                '--no-input',
            ]

            call_command(*call_args)

            if self.interactive:
                self.stdout.write(self.style.SUCCESS('OK'))
                self.stdout.write("\n")
