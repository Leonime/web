from django.conf import settings
from django.urls import path

from chirp.views import Index, ChirpListView, ChirpCreateView

app_name = 'chirp'
urlpatterns = [
    path('chipper/', Index.as_view(), name='index'),
    path('chipper/chirps/', ChirpListView.as_view(), name='chirps'),
    path('chipper/create-chirp/', ChirpCreateView.as_view(), name='create_chirp'),
]
