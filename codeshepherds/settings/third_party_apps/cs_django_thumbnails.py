from .redis import REDIS_URL, REDIS_PORT

THUMBNAILS_PROCESSORS = 'thumbnails.processors.resize'
THUMBNAILS_POST_PROCESSORS = {'PATH': 'thumbnails.post_processors.optimize', 'png_command': 'optipng %(filename)s'},

THUMBNAILS = {
    'METADATA': {
        'PREFIX': 'thumbs',
        'BACKEND': 'thumbnails.backends.metadata.RedisBackend',
        'db': 2,
        'port': REDIS_PORT,
        'host': f'{REDIS_URL}',
    },
    'STORAGE': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'BASE_DIR': 'thumbs',
    'SIZES': {
        'small': {
            'PROCESSORS': [
                {'PATH': THUMBNAILS_PROCESSORS, 'width': 10, 'height': 10}
            ],
            'POST_PROCESSORS': [
                THUMBNAILS_POST_PROCESSORS
            ]
        },
        'default': {
            'PROCESSORS': [
                {'PATH': THUMBNAILS_PROCESSORS, 'width': 50, 'height': 50},
            ],
            'POST_PROCESSORS': [
                THUMBNAILS_POST_PROCESSORS
            ]
        },
        'large': {
            'PROCESSORS': [
                {'PATH': THUMBNAILS_PROCESSORS, 'width': 100, 'height': 100},
            ],
            'POST_PROCESSORS': [
                THUMBNAILS_POST_PROCESSORS
            ]
        },
    }
}
