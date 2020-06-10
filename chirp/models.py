import random

from django.db import models


class Chirp(models.Model):
    content = models.TextField(null=False, blank=False)
    image = models.FileField()

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }