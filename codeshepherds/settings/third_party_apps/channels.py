import re

from codeshepherds.settings.django import SECRET_KEY
from .redis import REDIS_URL

############
# channels #
############
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
