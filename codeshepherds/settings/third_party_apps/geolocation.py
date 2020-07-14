import os

from codeshepherds.settings.django import BASE_DIR

###############
# Geolocation #
###############
GEOIP_PATH = os.path.join(BASE_DIR, 'analytics', 'GeoIP')
GEOIP_COUNTRY = 'GeoLite2-Country.mmdb'
GEOIP_CITY = 'GeoLite2-City.mmdb'
