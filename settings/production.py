from settings.base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

ALLOWED_HOSTS.append('.codeshepherds.com')
