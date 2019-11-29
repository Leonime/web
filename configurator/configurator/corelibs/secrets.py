import sys
from pathlib import Path

from configurator import ENV_SECRETS_DIR, BASE_DIR
from configurator.corelibs.utils import get_input


class SecretsFolder:
    def __init__(self, interactive=None, verbosity=None):
        self.interactive = interactive
        self.verbosity = verbosity

    def create_secrets_folder(self, base_dir, secrets_folder):
        custom_dir = base_dir / secrets_folder
        if not custom_dir.exists():
            print(f'Secrets folder "{secrets_folder}" doesn\'t exist on "{base_dir}" it will be created now.')
            if self.interactive:
                if get_input(confirmation=True, msg='Want to create folder?'):
                    custom_dir.mkdir()
                else:
                    sys.exit()
            else:
                if self.verbosity:
                    print(f'Creating directory "{custom_dir}"...')
                custom_dir.mkdir()
                if self.verbosity:
                    print(f'"{custom_dir}", directory created.')
        else:
            if not custom_dir.is_dir():
                raise Exception(f'{secrets_folder} is not a working path')
            if self.verbosity:
                print(f'Secrets folder has been set to "{custom_dir}"')
        return custom_dir

    def set_secrets_folder(self, args=None):
        custom_dir = None
        if args.path is not None and args.folder is not None:
            base_dir = Path(args.path)
            secrets_folder = Path(args.folder)
            if base_dir.is_dir():
                custom_dir = self.create_secrets_folder(base_dir, secrets_folder)
            else:
                raise Exception(f'{args.path} is not a directory')
        else:
            if args.path:
                base_dir = Path(args.path)
                if base_dir.is_dir():
                    custom_dir = base_dir.joinpath(ENV_SECRETS_DIR)
                else:
                    raise Exception(f'"{args.path}" is not a working path')
            if args.folder:
                base_dir = Path(BASE_DIR)
                secrets_folder = Path(args.folder)
                custom_dir = self.create_secrets_folder(base_dir, secrets_folder)
        if custom_dir is None:
            custom_dir = Path.joinpath(BASE_DIR, ENV_SECRETS_DIR)
        return custom_dir
