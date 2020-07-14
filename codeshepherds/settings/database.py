import os

from core.utils import load_db_config
from .django import BASE_DIR

######################
# Config file to use #
######################
CONFIG_FILE = os.environ.get('CONFIG_FILE')

config = load_db_config(BASE_DIR)

############
# Database #
############
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {}
}

if 'TRAVIS' not in os.environ:
    DATABASES['default'] = {
        'ENGINE': config['DB']['ENGINE'],
        'NAME': config['DB']['NAME'],
        'USER': config['DB']['USER'],
        'PASSWORD': config['DB']['PASSWORD'],
        'HOST': config['DB']['HOST'],
        'PORT': config['DB']['PORT'],
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travis_ci_test',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
