import base64
import os
import uuid
from pathlib import Path

from cryptography.fernet import InvalidToken, Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.test import TestCase

from core.utils import save_config_file, load_config_file, load_db_config

CONFIG_FILE = 'test_development.json'


class TestDecrypt(TestCase):
    @staticmethod
    def get_fernet(crypt_key):
        password = crypt_key
        salt = b'Jc2K2QCCh7T2QFNfCsES7TTkv8f8cmRebTyRCrmjV7CmZBmHxW'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))

        return Fernet(key)


class TestSaveConfigFile(TestCase):
    def setUp(self):
        config_file = CONFIG_FILE
        base_dir = os.environ.get('CODESHEPHERDS_BASE_DIR')
        self.path = Path(base_dir).joinpath(config_file)

    def test_save_config_file(self):
        save_config_file(self.path.name)
        self.assertTrue(self.path.is_file())

    def tearDown(self):
        self.path.unlink()


class TestLoadConfigFile(TestCase):
    def setUp(self):
        self.config_file = os.environ.get('CONFIG_FILE')

        config_file = CONFIG_FILE
        base_dir = os.environ.get('CODESHEPHERDS_BASE_DIR')
        os.environ['CONFIG_FILE'] = config_file
        self.path = Path(base_dir).joinpath(config_file)

    def test_load_config_file(self):
        config = load_config_file()
        self.assertTrue(self.path.is_file())
        self.assertEqual(load_config_file(), config)

    def tearDown(self):
        self.path.unlink()
        os.environ['CONFIG_FILE'] = self.config_file


class TestLoadDBConfig(TestCase):
    def setUp(self):
        self.config_file = os.environ.get('CONFIG_FILE')

        config_file = CONFIG_FILE
        base_dir = os.environ.get('CODESHEPHERDS_BASE_DIR')
        os.environ['CONFIG_FILE'] = config_file
        self.crypt_key = os.environ.get('CRYPT_KEY')
        self.path = Path(base_dir).joinpath(config_file)

        self.config = {'DB': {'NAME': 'codeshepherds',
                              'USER': 'leonime',
                              'PASSWORD': 'nomas123',
                              'HOST': 'localhost',
                              'PORT': ''}}

    def test_load_db_config(self):
        self.assertDictEqual(load_db_config(), self.config)
        os.environ['CRYPT_KEY'] = 'bad token'
        self.assertRaises(InvalidToken, lambda: load_db_config())

    def tearDown(self):
        self.path.unlink()
        os.environ['CRYPT_KEY'] = self.crypt_key
        os.environ['CONFIG_FILE'] = self.config_file
