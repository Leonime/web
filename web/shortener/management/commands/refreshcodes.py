from django.core.management.base import BaseCommand, CommandError

from shortener.models import ShortURL


class Command(BaseCommand):
    help = 'Refreshes all short codes'

    def handle(self, *args, **options):
        try:
            result = ShortURL.objects.refresh_short_codes()
        except ShortURL.DoesNotExist:
            raise CommandError('Entry does not exist')
        except Exception as e:
            raise CommandError(f'And error occurred: {e}')
        self.stdout.write(self.style.SUCCESS(result))
