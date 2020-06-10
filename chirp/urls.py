from django.urls import path

from chirp.views import Index, ChirpListView

app_name = 'chirp'
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('chirps/', ChirpListView.as_view(), name='chirps'),
]
