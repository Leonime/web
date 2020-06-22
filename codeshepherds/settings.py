"""
Django settings for codeshepherds project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
import logging.config
import os
import re

import sentry_sdk
from django.utils.log import DEFAULT_LOGGING
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from codeshepherds import version
from core.utils import load_db_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('CODESHEPHERDS_BASE_DIR', BASE_DIR)

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
SITE_ROOT = PROJECT_ROOT

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# Encryption key
CRYPT_KEY = os.environ.get('CRYPT_KEY')

# Config file to use
CONFIG_FILE = os.environ.get('CONFIG_FILE')

# Dropbox access key
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', default=False))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

SITE_ID = 1

# Redis url
REDIS_URL = os.environ.get('REDIS_URL')

# Auth urls defaults
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Installed apps
PRIORITY_APPS = [
    'channels',
    'whitenoise.runserver_nostatic',
]
# Default apps
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]
# Third party apps.
THIRD_PARTY_APPS = [
    'bootstrap4',
    'debug_toolbar',
    'django_extensions',
    'django_icons',
    'rest_framework',
    'widget_tweaks',
    'corsheaders',
    'crispy_forms',
]
# Local Apps
LOCAL_APPS = [
    'analytics.apps.AnalyticsConfig',
    'base.apps.BaseConfig',
    'chat.apps.ChatConfig',
    'chirp.apps.ChirpConfig',
    'cookbook.apps.CookbookConfig',
    'frontend.apps.FrontendConfig',
    'home.apps.HomeConfig',
    'party.apps.PartyConfig',
    'profiles.apps.ProfilesConfig',
    'shortener.apps.ShortenerConfig',
    'testing.apps.TestingConfig',
    'thumbnailer.apps.ThumbnailerConfig',
]
# Application definition
INSTALLED_APPS = PRIORITY_APPS + DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'codeshepherds.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'codeshepherds.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Media root path
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Images root path
IMAGES_DIR = os.path.join(MEDIA_ROOT, 'images')

if not os.path.exists(MEDIA_ROOT) or not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# URL prefix for static files.
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Geolocation
GEOIP_PATH = os.path.join(BASE_DIR, 'analytics', 'GeoIP')
GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'
GEOIP_CITY = 'GeoLite2-City.mmdb'

# Settings for django-icons
DJANGO_ICONS = {
    'DEFAULTS': {
        'renderer': 'fontawesome',
    },

    'RENDERERS': {
        'fontawesome': 'FontAwesomeRenderer',
        'bootstrap3': 'Bootstrap3Renderer',
    },

}

config = load_db_config(BASE_DIR)

# Database
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

# Apps custom settings
# Shortener
SHORT_CODE_MAX = 16
SHORT_CODE_MIN = 8

# Chipper
MAX_CHIRP_LENGTH = 240
CHIRP_ACTION_OPTIONS = ["chirp", "unchirp", "rechirp"]

# django-extensions settings
RUNSERVERPLUS_POLLER_RELOADER_INTERVAL = 5
RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8000'

GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

# Sentry
sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()]
)

# Logging
LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # root logger
        '': {
            'level': LOGLEVEL,
            'handlers': ['console', ],
        },
        'codeshepherds': {
            'level': LOGLEVEL,
            'handlers': ['console', ],
            # required to avoid double logging with root logger
            'propagate': False,
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
        'werkzeug': {
            'handlers': ['console', ],
            'level': LOGLEVEL,
            'propagate': True,
        },
    },
})

# celery
CELERY_BROKER_URL = f'redis://{REDIS_URL}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_URL}'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

# django toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG
}

# redis_cache
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': f'redis://{REDIS_URL}/',
        'OPTIONS': {
            'DB': 1,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 50,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'PICKLE_VERSION': -1,
        },
        'KEY_PREFIX': 'codeshepherds'
    }
}

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15

# Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# channels
ASGI_APPLICATION = 'codeshepherds.routing.application'

# channels_redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [f'redis://{REDIS_URL}/'],
            "symmetric_encryption_keys": [SECRET_KEY],
            'channel_capacity': {
                'http.request': 200,
                'http.response!*': 10,
                re.compile(r'^websocket.send!.+'): 20,
            },
        },
    },
}

# REST Framework
DEFAULT_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]

if DEBUG:
    DEFAULT_RENDERER_CLASSES += [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAdminUser', ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication', ],
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'PAGE_SIZE': 100
}

API_URL = 'api/v1/'

# Cors
CORS_ORIGIN_ALLOW_ALL = True  # any website has access to my api
CORS_URLS_REGEX = r'^/api/.*$'

# django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'
