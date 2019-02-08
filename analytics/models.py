from django.db import models

from shortener.models import ShortURL


class SURLAnalyticsManager(models.Manager):
    def create_event(self, instance, geolocation):
        if isinstance(instance, ShortURL):
            obj, created = self.get_or_create(short_url=instance)
            obj.count += 1
            obj.geolocation_set.create(ipv4=geolocation['ipv4'],
                                       city=geolocation['city'],
                                       country_code=geolocation['country_code'],
                                       country=geolocation['country'],
                                       found=geolocation['found'])
            obj.save()
            return obj.count
        return None


class SURLAnalytics(models.Model):
    short_url = models.OneToOneField(ShortURL, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = SURLAnalyticsManager()

    def __str__(self):
        return f'{self.count}'

    def __unicode__(self):
        return f'{self.count}'


class GeoLocation(models.Model):
    ipv4 = models.CharField(max_length=16, null=True)
    city = models.CharField(max_length=256, null=True)
    country_code = models.CharField(max_length=4, null=True)
    country = models.CharField(max_length=64, null=True)
    found = models.BooleanField(null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    surl_analytics = models.ForeignKey(SURLAnalytics, on_delete=models.CASCADE)

    objects = SURLAnalyticsManager()

    def __str__(self):
        return f'{self.country}'

    def __unicode__(self):
        return f'{self.country}'
