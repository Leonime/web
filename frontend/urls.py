from django.urls import path

from frontend.views import Index, ChirpDetail

app_name = 'frontend'
urlpatterns = [
    path('frontend/', Index.as_view(), name='index'),
    path('frontend/<int:chirp_id>/', ChirpDetail.as_view(), name='chirp_detail'),
]
