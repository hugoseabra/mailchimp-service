from django.core.management.base import BaseCommand

from namespace.tasks import validate_namespace
from .namespace_command_mixin import NamespaceCommandCommandMixin


class Command(NamespaceCommandCommandMixin, BaseCommand):
    help = "Validates namespace if it is still valid."

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

        namespace = self._get_namespace(
            options.get('api_key'),
            options.get('external_id')
        )

        if self.interactive:
            self.stdout.write("\n")
            self.stdout.write(self.style.SUCCESS('aguarde...'))
            self.stdout.write("\n")

        try:
            validate_namespace.delay(namespace_pk=namespace.pk,
                                     force_validation=self.force_validation)

            if self.interactive:
                self.stdout.writelines([
                    self.style.SUCCESS(
                        'Namespace "{}" processado.'.format(namespace.name)
                    ),
                    self.style.SUCCESS(
                        'Válido: {}'.format(
                            'Sim' if namespace.healthy else 'Não'
                        )
                    ),
                ])

        except Exception as e:
            self.stderr.write(str(e))
