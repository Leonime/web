import random

from django.contrib.auth.models import User
from django.db import models


class ChirpLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Chirp", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Chirp(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    likes = models.ManyToManyField(User, related_name='chirp_user', blank=True, through=ChirpLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/chipper/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.content}'

    @property
    def is_rechirp(self):
        return self.parent is not None

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
