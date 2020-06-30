import os

####################################################################
# SECURITY WARNING: keep the secret key used in production secret! #
####################################################################
SECRET_KEY = os.environ.get('SECRET_KEY')

##################
# Encryption key #
##################
CRYPT_KEY = os.environ.get('CRYPT_KEY')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('CODESHEPHERDS_BASE_DIR', BASE_DIR)

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
SITE_ROOT = PROJECT_ROOT

###################################################################
# SECURITY WARNING: don't run with debug turned on in production! #
###################################################################
DEBUG = int(os.environ.get('DEBUG', default=False))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')

SITE_ID = 1

MIDDLEWARE = [
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

WSGI_APPLICATION = 'codeshepherds.wsgi.application'

######################################################
# Internationalization                               #
# https://docs.djangoproject.com/en/1.9/topics/i18n/ #
######################################################
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
