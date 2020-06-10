from django.urls import path

from chirp.views import Index, ChirpListView, ChirpCreateView

app_name = 'chirp'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('chirps/', ChirpListView.as_view(), name='chirps'),
    path('create-chirp/', ChirpCreateView.as_view(), name='create_chirp'),
]
