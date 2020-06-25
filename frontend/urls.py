from django.urls import path

from frontend.views import ChirpDetail, ChirpList, ProfileDetail

app_name = 'frontend'
urlpatterns = [
    path('frontend/', ChirpList.as_view(), name='chirp_list'),
    path('frontend/<int:chirp_id>/', ChirpDetail.as_view(), name='chirp_detail'),
    path('frontend/profile/<str:username>/', ProfileDetail.as_view(), name='profile_detail'),
]
