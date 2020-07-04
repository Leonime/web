from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from chirp.models import Chirp, ChirpLike


class ChirpLikeAdmin(admin.TabularInline):
    model = ChirpLike


class ChirpAdmin(SimpleHistoryAdmin):
    inlines = [ChirpLikeAdmin]
    list_display = ['user', '__str__']
    search_fields = ['content', 'user__username', 'user__email']

    class Meta:
        model = Chirp


admin.site.register(Chirp, ChirpAdmin)
