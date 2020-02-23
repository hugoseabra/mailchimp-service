from django.core.management.base import BaseCommand

from audience.service import sync_member
from namespace.management.commands.namespace_command_mixin import \
    NamespaceCommandCommandMixin


class Command(NamespaceCommandCommandMixin, BaseCommand):
    help = "Synchronizes members of a namespace which are not already" \
           " synchronized according to sychronization types."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        self.process_options(options)

        namespace = self._get_namespace(
            options.get('api_key'),
            options.get('external_id')
        )

        members = namespace.members.filter(synchronized=False)

        num = members.count()

        try:
            if num == 0:
                raise Exception(
                    '{}: No members to synchronize'.format(namespace.name)
                )

            if self.interactive:
                self.stdout.write("\n")
                self.stdout.write(self.style.SUCCESS('aguarde...'))
                self.stdout.write("\n")

            if num:
                for m in members:
                    if self.interactive:
                        self.stdout.write(
                            '  - {} ({}): '.format(
                                m.full_name,
                                m.external_id,
                            ),
                            ending='',
                        )

                    sync_member(m)

                    if self.interactive:
                        self.stdout.write(self.style.SUCCESS('OK'))
                        self.stdout.write("\n")

        except Exception as e:
            self.stderr.write(str(e))
