import logging
from pathlib import Path
from zipfile import ZipFile

from PIL import Image
from celery import shared_task
from django.conf import settings


@shared_task
def make_thumbnails(file_path, thumbnails=None):
    logger = logging.getLogger(__name__)

    if thumbnails is None:
        thumbnails = []

    image_dir = Path(settings.IMAGES_DIR)
    file = Path(file_path)

    zip_file = f"{file.stem}.zip"
    results = {
        'archive_path': f'{settings.MEDIA_URL}images/{zip_file}',
        'archive_name': f'{zip_file}',
    }
    try:
        with Image.open(file) as img:
            with ZipFile(image_dir / zip_file, 'w') as zipper:
                zipper.write(file)
                file.unlink()
                for w, h in thumbnails:
                    img_copy = img.copy()
                    img_copy.thumbnail((w, h))
                    thumbnail_file = image_dir / f'{file.stem}_{w}x{h}.{file.suffix}'
                    img_copy.save(thumbnail_file)
                    zipper.write(thumbnail_file)
                    thumbnail_file.unlink()
    except IOError as e:
        logger.error(e)

    return results
