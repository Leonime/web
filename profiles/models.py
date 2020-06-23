from django.contrib.auth.models import User
from django.db import models


class FollowerRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text='The user')
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE, help_text='The user profile')
    timestamp = models.DateTimeField(auto_now_add=True, help_text='A record keeping timestamp.')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text='The user')
    location = models.CharField(max_length=220, null=True, blank=True, help_text='The user location')
    bio = models.TextField(blank=True, null=True, help_text='The user bio')
    followers = models.ManyToManyField(User, related_name='following', blank=True, help_text='The user followers')
