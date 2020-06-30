from .redis import REDIS_URL

##########
# celery #
##########
CELERY_BROKER_URL = f'redis://{REDIS_URL}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_URL}'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
