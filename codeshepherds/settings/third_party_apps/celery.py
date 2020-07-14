from .redis import REDIS

##########
# celery #
##########
CELERY_BROKER_URL = f'redis://{REDIS}'
CELERY_RESULT_BACKEND = f'redis://{REDIS}'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
