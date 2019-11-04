import sys

import dropbox
from colorama import Fore, Style
from django.conf import settings
from django.core.management import BaseCommand
from django.template.defaultfilters import filesizeformat
from pathlib import Path


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geoip_path = getattr(settings, "GEOIP_PATH", None)
        self.dropbox_access_token = getattr(settings, "DROPBOX_ACCESS_TOKEN", '')
        pass

    def handle(self, *args, **options):
        dbx = dropbox.Dropbox(self.dropbox_access_token)
        dbx.users_get_current_account()
        for entry in dbx.files_list_folder('/GeoIP').entries:
            print(Style.RESET_ALL + entry.name)
            save_location = Path(self.geoip_path).joinpath(entry.name)
            with open(save_location, 'wb') as f:
                metadata, response = dbx.files_download(path=entry.path_display)
                total = int(response.headers.get('content-length'))
                downloaded = 0
                for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                    downloaded += len(data)
                    f.write(data)
                    done = int(30 * downloaded / total)
                    sys.stdout.write(
                        f'\r[{Fore.GREEN + ("█" * done)}'
                        f'{Fore.BLACK + ("█" * (30 - done)) + Style.RESET_ALL}]'
                        f' {filesizeformat(downloaded)}/{filesizeformat(total)}')
                    sys.stdout.flush()
                    pass
                sys.stdout.write('\n')
                pass
            pass
        return True

    help = 'Updates geolocation DB'
