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
from django.conf import settings

from codeshepherds.settings import BASE_DIR

_MAX_CLOCK_SKEW = 60


def decrypt(self, token, ttl=None):
    current_time = int(time.time())
    if not isinstance(token, bytes):
        raise TypeError('token must be bytes.')

    try:
        data = base64.urlsafe_b64decode(token)
    except (TypeError, binascii.Error):
        raise InvalidToken

    if not data or six.indexbytes(data, 0) != 0x80:
        raise InvalidToken

    try:
        timestamp, = struct.unpack('>Q', data[1:9])
    except struct.error:
        raise InvalidToken

    if ttl is not None:
        if timestamp + ttl < current_time:
            raise InvalidToken
    if current_time + _MAX_CLOCK_SKEW < timestamp:
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
    try:
        plaintext_padded += decrypter.finalize()
    except ValueError:
        raise InvalidToken
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    unpadded = unpadder.update(plaintext_padded)
    try:
        unpadded += unpadder.finalize()
    except ValueError:
        raise InvalidToken
    return unpadded.decode('utf-8')


def load_db_config():
    config_file = getattr(settings, "CONFIG_FILE", 'development.json')
    password = str.encode(os.environ.get('CRYPT_KEY'))
    salt = b'd\x04\xe7@T\xd6\x8e\xac\xa5\xd9\xfb\x17o\xc0\xc2g'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    with open(os.path.join(BASE_DIR, config_file), 'r') as cfg:
        config = json.load(cfg)

    config = {
        k: {
            k: f.decrypt(str(v).encode('utf-8')).decode('utf-8')
            for k, v in v.items()
        }
        for k, v in config.items()
    }

    return config
