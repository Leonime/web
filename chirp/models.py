from django.db import models


class Chirp(models.Model):
    content = models.TextField()
    image = models.FileField()
