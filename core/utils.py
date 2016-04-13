import base64
import struct
import time

import binascii

import six
from cryptography.exceptions import InvalidSignature
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC

_MAX_CLOCK_SKEW = 60


def decrypt(self, token, ttl=None):
    current_time = int(time.time())
    if not isinstance(token, bytes):
        raise TypeError("token must be bytes.")

    try:
        data = base64.urlsafe_b64decode(token)
    except (TypeError, binascii.Error):
        raise InvalidToken

    if not data or six.indexbytes(data, 0) != 0x80:
        raise InvalidToken

    try:
        timestamp, = struct.unpack(">Q", data[1:9])
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
    return unpadded.decode("utf-8")
