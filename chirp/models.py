import random

from django.contrib.auth.models import User
from django.db import models


class ChirpLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Chirp", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Chirp(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL, help_text='The parent chirp.')
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, help_text='Who is the owner of the chirp.')
    likes = models.ManyToManyField(User, related_name='chirp_user', blank=True, through=ChirpLike,
                                   help_text='It keeps a record on who likes the chirp.')
    content = models.TextField(blank=True, null=True, help_text='The content of the chirp.')
    image = models.FileField(upload_to='images/chipper/', blank=True, null=True, help_text='An image.')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='The time when the chirp was created.')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.content}'

    @property
    def is_rechirp(self):
        return self.parent is not None
