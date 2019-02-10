from core.utils import load_db_config
from settings.base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS = ['.codeshepherds.com', '.testdevsheep.herokuapp.com']

config = load_db_config()

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config["DB"]["NAME"],
        'USER': config["DB"]["USER"],
        'PASSWORD': config["DB"]["PASSWORD"],
        'HOST': config["DB"]["HOST"],
        'PORT': config["DB"]["PORT"],
    }
}
