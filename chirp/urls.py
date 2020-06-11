from django.urls import path

from chirp.views import Index, ChirpCreateView

app_name = 'chirp'
urlpatterns = [
    path('chipper/', Index.as_view(), name='index'),
    path('chipper/create-chirp/', ChirpCreateView.as_view(), name='create_chirp'),
]
