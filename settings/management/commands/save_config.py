from django.conf import settings
from django.core.management import BaseCommand

from core.utils import save_config_file


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_file = getattr(settings, "CONFIG_FILE", None)

    def add_arguments(self, parser):
        parser.add_argument(
            '--default',
            action='store_true',
            dest='default',
            help='Save default config file.',
        )

    def handle(self, *args, **options):
        if options['default']:
            save_config_file(self.config_file)

            self.stdout.write(self.style.SUCCESS(f'Save file "{self.config_file}" created.'))
            pass
        else:
            pass
        pass

    help = 'Creates config file'
