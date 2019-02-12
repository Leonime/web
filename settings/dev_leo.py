import django_heroku

from settings.base import *

ALLOWED_HOSTS.append('localhost')
ALLOWED_HOSTS.append('.codeshepherds.com')
ALLOWED_HOSTS.append('.testdevsheep.herokuapp.com')

# Activate Django-Heroku.
django_heroku.settings(locals())
