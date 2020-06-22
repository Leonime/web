from django.urls import path

from frontend.views import ChirpDetail, ChirpList

app_name = 'frontend'
urlpatterns = [
    path('frontend/', ChirpList.as_view(), name='chirp_list'),
    path('frontend/<int:chirp_id>/', ChirpDetail.as_view(), name='chirp_detail'),
]
