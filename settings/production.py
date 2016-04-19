import base64
import json

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from core.utils import decrypt
from settings.base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ['.codeshepherds.com']

with open(os.path.join(BASE_DIR, "config.json"), 'r') as cfg:
    config = json.load(cfg)

password = str.encode(CRYPT_KEY)
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

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': decrypt(f, str.encode(config["DB"]["NAME"])),
        'USER': decrypt(f, str.encode(config["DB"]["USER"])),
        'PASSWORD': decrypt(f, str.encode(config["DB"]["PASSWORD"])),
        'HOST': decrypt(f, str.encode(config["DB"]["HOST"])),
        'PORT': '',
    }
}
