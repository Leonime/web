from django.conf import settings
from django.urls import path, include

from chirp.api.routers import chirp_router
from chirp.views import Index, ChirpCreateView

app_name = 'chirp'
urlpatterns = [
    path('chipper/', Index.as_view(), name='index'),
    path('chipper/create-chirp/', ChirpCreateView.as_view(), name='create_chirp'),
    path(f'{settings.API_URL}', include(chirp_router.urls)),
]
