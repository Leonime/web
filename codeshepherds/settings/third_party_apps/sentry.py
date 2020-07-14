import os

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from codeshepherds.settings.django import DEBUG

if not DEBUG:
    ##########
    # Sentry #
    ##########
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[DjangoIntegration(), CeleryIntegration(), RedisIntegration()]
    )
