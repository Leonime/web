from codeshepherds.celery import celery_app

version_info = ('0', '7', '10')
version = '.'.join(version_info)

__all__ = ('celery_app', version)
