from django.contrib import admin

from chirp.models import Chirp


class ChirpAdmin(admin.ModelAdmin):
    list_display = ['user', '__str__']
    search_fields = ['user__username', 'user__email']

    class Meta:
        model = Chirp


admin.site.register(Chirp, ChirpAdmin)
