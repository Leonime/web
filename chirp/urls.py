from django.urls import path
from django.conf import settings

from chirp.views import Index, ChirpListView, ChirpCreateView, ChirpList, ChirpDetail

app_name = 'chirp'
api_url = f'{settings.API_URL}chipper/'
urlpatterns = [
    path('chipper/', Index.as_view(), name='index'),
    path('chipper/chirps/', ChirpListView.as_view(), name='chirps'),
    path('chipper/create-chirp/', ChirpCreateView.as_view(), name='create_chirp'),
    path(f'{api_url}chirps/', ChirpList.as_view(), name='ChirpList'),
    path(f'{api_url}chirps/<int:pk>/', ChirpDetail.as_view(), name='ChirpDetail'),
]
