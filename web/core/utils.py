import binascii
import time

import base64
import json
import os
import six
import struct
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken, Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pathlib import Path


def decrypt(self, token, ttl=None, max_clock_skew=60):
    current_time = int(time.time())
    if not isinstance(token, bytes):
        raise TypeError('token must be bytes.')

    try:
        data = base64.urlsafe_b64decode(token)
    except (TypeError, binascii.Error):
        raise InvalidToken

    if not data or six.indexbytes(data, 0) != 0x80:
        raise InvalidToken

    timestamp, = struct.unpack('>Q', data[1:9])

    if ttl and not isinstance(ttl, int):
        raise TypeError('ttl must be int')

    if ttl is not None:
        if timestamp + ttl < current_time:
            raise InvalidToken
    if current_time + max_clock_skew < timestamp:
        raise InvalidToken

    h = HMAC(self._signing_key, hashes.SHA256(), backend=self._backend)
    h.update(data[:-32])

    try:
        h.verify(data[-32:])
    except InvalidSignature:
        raise InvalidToken

    iv = data[9:25]

    cipher_text = data[25:-32]
    decrypter = Cipher(
        algorithms.AES(self._encryption_key), modes.CBC(iv), self._backend
    ).decryptor()
    plaintext_padded = decrypter.update(cipher_text)
    plaintext_padded += decrypter.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded = unpadder.update(plaintext_padded)
    unpadded += unpadder.finalize()

    return unpadded.decode('utf-8')


def create_encryptor():
    crypt_key = os.environ.get('CRYPT_KEY')
    password = str.encode(crypt_key)
    crypt_salt = str(os.environ.get('CRYPT_SALT'))
    salt = str.encode(crypt_salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA512(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)


def save_config_file(config_file='development.json',
                     name='codeshepherds',
                     user='leonime',
                     password='nomas123',
                     host='localhost',
                     port=''):
    base_dir = os.environ.get('CODESHEPHERDS_BASE_DIR')
    path = Path(base_dir).joinpath(config_file)
    f = create_encryptor()

    json_data = {'DB': {}}

    json_data['DB']['NAME'] = f.encrypt(str.encode(name)).decode('utf-8')
    json_data['DB']['USER'] = f.encrypt(str.encode(user)).decode('utf-8')
    json_data['DB']['PASSWORD'] = f.encrypt(str.encode(password)).decode('utf-8')
    json_data['DB']['HOST'] = f.encrypt(str.encode(host)).decode('utf-8')
    json_data['DB']['PORT'] = f.encrypt(str.encode(port)).decode('utf-8')

    with path.open('w') as file:
        json.dump(json_data, file, sort_keys=True, indent=4)
        pass
    pass


def load_config_file():
    config_file = os.environ.get('CONFIG_FILE')
    base_dir = os.environ.get('CODESHEPHERDS_BASE_DIR')
    path = Path(base_dir).joinpath(config_file)

    if path.exists():
        with path.open() as cfg:
            config = json.load(cfg)
            pass
        pass
    else:
        save_config_file(config_file, 'codeshepherds', 'leonime', 'nomas123', 'localhost', '')
        config = load_config_file()
        pass
    return config


def load_config():
    config = {
        'DB': {
            'NAME': os.environ.get('SQL_DATABASE'),
            'USER': os.environ.get('SQL_USER'),
            'PASSWORD': os.environ.get('SQL_PASSWORD'),
            'HOST': os.environ.get('SQL_HOST'),
            'PORT': os.environ.get('SQL_PORT'),
        }
    }
    return config


def load_db_config():
    load_from_environment = bool(os.environ.get('LOAD_FROM_ENVIRONMENT', True))
    if load_from_environment:
        config = load_config()
    else:
        config = load_config_file()
    f = create_encryptor()

    try:
        config = {
            key: {
                key: f.decrypt(str(value).encode('utf-8')).decode('utf-8')
                for key, value in value.items()
            }
            for key, value in config.items()
        }
    except InvalidToken:
        raise InvalidToken

    return config
