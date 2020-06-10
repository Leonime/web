from django.contrib import admin

from chirp.models import Chirp, ChirpLike


class ChirpLikeAdmin(admin.TabularInline):
    model = ChirpLike


class ChirpAdmin(admin.ModelAdmin):
    inlines = [ChirpLikeAdmin]
    list_display = ['user', '__str__']
    search_fields = ['content', 'user__username', 'user__email']

    class Meta:
        model = Chirp


admin.site.register(Chirp, ChirpAdmin)
