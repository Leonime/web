import random

from django.contrib.auth.models import User
from django.db import models


class Chirp(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField(null=False, blank=False)
    image = models.FileField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.content}'

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
