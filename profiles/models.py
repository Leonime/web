from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='The user')
    location = models.CharField(max_length=220, null=True, blank=True, help_text='The user location')
    bio = models.TextField(blank=True, null=True, help_text='The user bio')
    followers = models.ManyToManyField(User, related_name='following', blank=True, help_text='The user followers')
    image = models.ImageField(upload_to='pictures/profile/%Y/%m/%d/',
                              max_length=512, blank=True, null=True, help_text='The profile picture')
