from django.contrib import admin

from analytics.models import SURLAnalytics, GeoLocation

admin.site.register(SURLAnalytics)
admin.site.register(GeoLocation)
