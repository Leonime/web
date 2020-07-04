from django.contrib import admin

from profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'bio', 'image_tag']
    readonly_fields = ['image_tag']


admin.site.register(Profile, ProfileAdmin)
