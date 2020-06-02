from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models import Weekday


class Testing(models.Model):
    dow = models.ManyToManyField(Weekday)

    def __str__(self):
        return ", ".join([item.description for item in self.dow.all()])
