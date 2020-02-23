from django.core.management import call_command
from django.core.management.base import BaseCommand

from namespace.models import Namespace
from .namespace_command_mixin import NamespaceCommandCommandMixin


class Command(NamespaceCommandCommandMixin, BaseCommand):
    help = "Validates all namespaces if it is still valid."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.force_validation = False

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '--force-validation', '--force-validation', action='store_true',
            dest='force_validation',
            help='Forces validation of namespace replacing the wrong list ID.',
        )

    def process_options(self, options: dict = None):
        super().process_options(options)
        self.force_validation = options.get('force_validation')

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
                'validate_namespace',
                namespace.api_key,
                namespace.external_id,
                '--no-input',
            ]

            if self.force_validation:
                call_args.append('--force-validation')

            call_command(*call_args)

            if self.interactive:
                self.stdout.write(self.style.SUCCESS('OK'))
                self.stdout.write("\n")
