from django.conf import settings
from django.core.management import BaseCommand
from getpass import getpass

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
        parser.add_argument(
            '--no-config-name',
            action='store_true',
            dest='no_config_name',
            help='Save default config file with file name from settings, if not set "development.json" will be used.',
        )

    def handle(self, *args, **options):
        if options['default']:
            save_config_file(self.config_file)

            self.stdout.write(self.style.SUCCESS(f'Save file "{self.config_file}" created.'))
            pass
        elif options['no_config_name']:
            name = self.get_input(msg='Enter DB name: ')
            user = self.get_input(msg='Enter DB user: ')
            password = self.get_input(is_pass=True, msg='Enter DB password: ')
            host = self.get_input(msg='Enter DB host: ')
            port = self.get_input(blank=True, msg='Enter DB port: ')

            save_config_file(self.config_file, name, user, password, host, port)

            self.stdout.write(self.style.SUCCESS(f'Save file "{self.config_file}" created.'))
            pass
        else:
            config_file = self.get_input(msg='Enter config file name: ')
            name = self.get_input(msg='Enter DB name: ')
            user = self.get_input(msg='Enter DB user: ')
            password = self.get_input(is_pass=True, msg='Enter DB password: ')
            host = self.get_input(msg='Enter DB host: ')
            port = self.get_input(blank=True, msg='Enter DB port: ')

            save_config_file(config_file, name, user, password, host, port)

            self.stdout.write(self.style.SUCCESS(f'Save file "{config_file}" created.'))
            pass
        pass

    def get_input(self, blank=False, is_pass=False, msg=''):
        value = None
        while value is None:
            if not is_pass:
                value = input(self.style.WARNING(msg))
                pass
            else:
                value = getpass(self.style.WARNING(msg))
                pass
            if not value and not blank:
                self.stdout.write(self.style.ERROR('Cannot be blank'))
                value = None
                pass
            pass
        return value

    help = 'Creates config file'
