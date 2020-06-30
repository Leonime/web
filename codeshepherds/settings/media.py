import os

from .django import BASE_DIR

###################
# Media root path #
###################
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

####################
# Images root path #
####################
IMAGES_DIR = os.path.join(MEDIA_ROOT, 'images')

if not os.path.exists(MEDIA_ROOT) or not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

#############################################################################
# URL that handles the media served from MEDIA_ROOT. Make sure to use a     #
# trailing slash.                                                           #
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/' #
#############################################################################
MEDIA_URL = '/media/'
