from .django import DEBUG, MIDDLEWARE
from .third_party_apps.django_rest_framework import DEFAULT_RENDERER_CLASSES
from .installed_apps import INSTALLED_APPS

if DEBUG:
    ########################
    # Django debug toolbar #
    ########################
    INTERNAL_IPS = [
        '127.0.0.1',
    ]

    INSTALLED_APPS += [
        'debug_toolbar',
        'django_extensions',
    ]
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG
    }

    ##################
    # REST Framework #
    ##################
    DEFAULT_RENDERER_CLASSES += [
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]

    ##############################
    # django-extensions settings #
    ##############################
    RUNSERVERPLUS_POLLER_RELOADER_INTERVAL = 5
    RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8000'

    GRAPH_MODELS = {
        'all_applications': True,
        'group_models': True,
    }
