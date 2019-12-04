import base64
import os
import uuid
from pathlib import Path

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from configurator.corelibs.environment_file import DotEnv


class Encryptor:
    def __init__(self):
        self.crypt_key = str(os.environ.get('CRYPT_KEY'))
        self.salt = str(os.environ.get('CRYPT_SALT'))
        if not self.salt:
            self.save_salt()

    def save_salt(self):
        self.salt = uuid.uuid4().hex
        dot_env = DotEnv()
        dot_env.set_environment_variable('CRYPT_SALT', self.salt)

    def create_encryptor(self):
        password = self.crypt_key.encode()
        salt = self.salt.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return Fernet(key)
