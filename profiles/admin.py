from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from profiles.models import Profile


class ProfileAdmin(SimpleHistoryAdmin):
    list_display = ['user', 'location', 'bio', 'image_tag']
    readonly_fields = ['image_tag']


admin.site.register(Profile, ProfileAdmin)
