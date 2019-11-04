from django.db import models


class Weekday(models.Model):
    description = models.CharField(max_length=12)

    def __str__(self):
        return self.description
