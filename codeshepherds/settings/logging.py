import logging.config
import os

from django.utils.log import DEFAULT_LOGGING

###########
# Logging #
###########
DJANGO_SERVER = 'django.server'
LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        DJANGO_SERVER: DEFAULT_LOGGING['formatters'][DJANGO_SERVER],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        DJANGO_SERVER: DEFAULT_LOGGING['handlers'][DJANGO_SERVER],
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
        DJANGO_SERVER: DEFAULT_LOGGING['loggers'][DJANGO_SERVER],
        'werkzeug': {
            'handlers': ['console', ],
            'level': LOGLEVEL,
            'propagate': True,
        },
    },
})
