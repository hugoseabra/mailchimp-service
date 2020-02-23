from core.cli.mixins import CliInteractionMixin
from namespace import models


class NamespaceCommandCommandMixin(CliInteractionMixin):
    def __init__(self, *args, **kwargs):
        self.interactive = True
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('api_key', type=str, nargs='?')
        parser.add_argument('external_id', type=str, nargs='?')
        parser.add_argument(
            '--noinput', '--no-input', action='store_false',
            dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    def process_options(self, options: dict = None):
        self.interactive = options.get('interactive')

    def _get_namespace(self, api_key: str = None, external_id: str = None):
        namespace = None

        while not namespace:
            if self.interactive is True:
                if api_key is None:
                    self.stdout.write("\n")
                    self.stdout.write(
                        "Informe o API Key (ou encerre com Ctrl+c)"
                    )
                    api_key = input("API Key: ")

                if external_id is None:
                    self.stdout.write("\n")
                    self.stdout.write(
                        "Informe o External ID (ou encerre com Ctrl+c)"
                    )
                    external_id = input("External ID: ")

            elif not api_key or not external_id:
                raise Exception('api_key or external_id not found.')

            try:
                namespace = self.get_namespace_instance(api_key, external_id)

                if self.interactive:
                    confirmed = self.confirmation_yesno(
                        'Confirmar o namespace encontrado encontrado?',
                        exit_on_false=False
                    )

                    if confirmed is False:
                        api_key = None
                        external_id = None
                        namespace = None

            except Exception as e:
                self.stderr.write(str(e))
                api_key = None
                external_id = None
                namespace = None

        return namespace

    def get_namespace_instance(self, api_key: str, external_id: str):
        try:
            instance = models.Namespace.objects.get(
                api_key=api_key.strip(),
                external_id=external_id.strip(),
            )

            if self.interactive:
                self.stdout.write(
                    '----------------------------------------------'
                )
                if len(instance.name) > 30:
                    self.stdout.write(
                        'NAMESPACE: ' + self.style.SUCCESS(
                            instance.name[:30] + '...')
                    )
                else:
                    self.stdout.write(
                        'NAMESPACE: ' + self.style.SUCCESS(instance.name)
                    )

                num = instance.members.filter(synchronized=False).count()

                self.stdout.write(
                    'Members to Synchronize: ' + self.style.SUCCESS(
                        num or '0'
                    )
                )

            return instance

        except models.Namespace.DoesNotExist as e:
            raise e
