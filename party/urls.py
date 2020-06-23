from django.conf import settings
from django.urls import path, include

from party.api.routers import party_router

app_name = 'chirp'
urlpatterns = [
    path(f'{settings.API_URL}', include(party_router.urls)),
]
