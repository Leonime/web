from django.contrib.admin import register
from django.contrib import admin
from django.contrib.auth.models import User, Permission, Group
from simple_history.admin import SimpleHistoryAdmin

admin.site.unregister(User)
admin.site.unregister(Group)


@register(User)
class UserAdmin(SimpleHistoryAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']


@register(Permission)
class PermissionAdmin(SimpleHistoryAdmin):
    list_display = ['codename', 'name', 'content_type']


@register(Group)
class GroupAdmin(SimpleHistoryAdmin):
    list_display = ['name', 'get_permissions']

    def get_permissions(self, obj):
        return ', '.join([f'"{permission}"' for permission in obj.permissions.all()])
