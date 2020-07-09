import os

from core.utils import get_boolean

EMAIL_USE_TLS = get_boolean(os.environ.get('EMAIL_USE_TLS'))
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_SEND_EMAIL = os.environ.get('EMAIL_SEND_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
