from codeshepherds.celery import celery_app

version_info = ('0', '8', '1')
version = '.'.join(version_info)

__all__ = ('celery_app', version)
