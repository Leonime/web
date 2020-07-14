from django.contrib.auth.models import User, Permission, Group
from simple_history import register

register(User, app=__package__)
register(Permission, app=__package__)
register(Group, app=__package__)
