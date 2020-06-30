from codeshepherds.settings.django import DEBUG

##################
# REST Framework #
##################
DEFAULT_RENDERER_CLASSES = [
    'rest_framework.renderers.JSONRenderer',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAdminUser', ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication', ],
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    'PAGE_SIZE': 10 if DEBUG else 100
}

API_URL = 'api/v1/'
