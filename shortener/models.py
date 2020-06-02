from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse

from shortener.validators import validate_url
from shortener.utils import create_short_code

SHORT_CODE_MAX = getattr(settings, "SHORT_CODE_MAX", 16)


class ShortURLManager(models.Manager):
    @staticmethod
    def refresh_short_codes():
        qs = ShortURL.objects.filter(id__gte=1)
        new_codes = 0
        for q in qs:
            q.short_code = create_short_code(q)
            q.save()
            new_codes += 1
        return f"New codes made: {new_codes}"


# Create your models here.
class ShortURL(models.Model):
    url = models.CharField(max_length=2083, validators=[validate_url])
    short_code = models.CharField(max_length=SHORT_CODE_MAX, unique=True)
    updated = models.DateTimeField(auto_now=True)  # every time the model is saved
    timestamp = models.DateTimeField(auto_now_add=True)  # when model was created
    active = models.BooleanField(default=True)

    objects = ShortURLManager()

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = create_short_code(self)
        super(ShortURL, self).save(*args, **kwargs)
        pass

    def get_absolute_url(self):
        domain = Site.objects.get_current().domain
        return f"http://{domain}{reverse('shortener:short_code', kwargs={'short_code': self.short_code})}"

    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self)

    def __str__(self):
        domain = Site.objects.get_current().domain
        return f"http://{domain + reverse('short_code', kwargs={'short_code': self.short_code})}"
