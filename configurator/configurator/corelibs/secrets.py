import logging
import sys
from pathlib import Path

import docker
import yaml
from docker.errors import APIError, NotFound

from configurator import ENV_SECRETS_DIR, BASE_DIR
from configurator.corelibs.encryption import Encryptor
from configurator.corelibs.environment_file import DotEnv
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


class Secrets:
    def __init__(self, secret_path=Path(), interactive=None, verbosity=None):
        self.interactive = interactive
        self.verbosity = verbosity
        self.secret_path = secret_path
        self.yaml_file = Path().cwd().parent / 'docker-compose.yml'
        self.secrets_yml = {'secrets': {}}

        self.client = docker.from_env()

    def init_docker_swarm(self):
        if not self.client.swarm.id:
            try:
                swarm_id = self.client.swarm.init()
                print(f'Swarm created, id: "{swarm_id}"')
            except APIError as e:
                raise Exception(f'{e.explanation}')
            except Exception as e:
                logging.exception(e)
                raise Exception(f'{e}')

    def create_docker_secret(self, name=None, data=None):
        try:
            secret = self.client.secrets.get(name)
            if secret.id:
                secret.remove()
                self.client.secrets.create(name=name, data=data)
        except NotFound:
            self.client.secrets.create(name=name, data=data)

    def save_yaml(self):
        with open(str(self.yaml_file), 'w') as file:
            file.write(yaml.dump(self.secrets_yml))

    def create_text_secret(self, filename=str(), data=str()):
        if filename is None or data is None:
            raise Exception('Filename or data can\'t be None')
        with open(self.secret_path / filename, 'w') as file:
            file.write(data)

    def save_env_var(self, file_name=str(), data=str(), env_name=str(), encrypt=True, env=True, yaml=True):
        if encrypt:
            encryptor = Encryptor()
            f = encryptor.create_encryptor()
            data = f.encrypt(data.encode()).decode('utf-8')
        if env:
            dot_env = DotEnv()
            dot_env.set_environment_variable(env_name, file_name)
        if yaml:
            self.secrets_yml['secrets'].update({
                f'{file_name}': {
                    'file': f'./secrets/{file_name}'
                }
            })
        self.create_text_secret(file_name, data)

    def create_default(self, docker_secret=False):
        if docker_secret:
            # django secrets
            self.create_docker_secret('django_db_name', 'codeshepherds')
            self.create_docker_secret('django_db_password', 'nomas123')
            self.create_docker_secret('django_db_port', '5432')
            self.create_docker_secret('django_db_user', 'leonime')
            self.create_docker_secret('django_db_host', 'postgres')
            self.create_docker_secret('django_db_engine', 'django.db.backends.postgresql')
        else:
            self.save_env_var('django_db_name', 'codeshepherds', 'SQL_DATABASE')
            self.save_env_var('django_db_password', 'nomas123', 'SQL_PASSWORD')
            self.save_env_var('django_db_port', '5432', 'SQL_PORT')
            self.save_env_var('django_db_user', 'leonime', 'SQL_USER')
            self.save_env_var('django_db_host', 'postgres', 'SQL_HOST')
            self.save_env_var('django_db_host_dev', 'postgres_dev', 'SQL_HOST')
            self.save_env_var('django_db_engine', 'django.db.backends.postgresql', 'SQL_ENGINE')

            kwargs = {
                'encrypt': False,
                'env': True
            }
            self.save_env_var('django_su_name', 'Leonime', 'DJANGO_SU_NAME', **kwargs)
            self.save_env_var('django_su_email', 'lparra.dev@gmail.com', 'DJANGO_SU_EMAIL', **kwargs)
            self.save_env_var('django_su_password', 'nomas123', 'DJANGO_SU_PASSWORD', **kwargs)

            kwargs = {
                'env_name': '',
                'encrypt': False,
                'env': False
            }
            self.save_env_var('postgres_user', 'leonime', **kwargs)
            self.save_env_var('postgres_password', 'nomas123', **kwargs)
            self.save_env_var('postgres_database', 'codeshepherds', **kwargs)

            self.save_yaml()
