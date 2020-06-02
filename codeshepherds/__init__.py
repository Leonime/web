from codeshepherds.celery import celery_app

version_info = (0, 3, 0)
version = '.'.join(str(c) for c in version_info)

__all__ = ('celery_app', version)
