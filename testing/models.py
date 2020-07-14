from django.db import models
from thumbnails import fields

from base.models import Weekday


class Testing(models.Model):
    dow = models.ManyToManyField(Weekday)

    def __str__(self):
        return ", ".join([item.description for item in self.dow.all()])


class Gallery(models.Model):
    image = fields.ImageField(upload_to='pictures/profile/%Y/%m/%d/',
                              blank=True, null=True, help_text='The picture')
