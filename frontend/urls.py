from django.urls import path

from frontend.views import ChirpDetail, ChirpList, ProfileDetail, ChirpFrontPageView
from profiles.views import UserProfileDetailView

app_name = 'frontend'
urlpatterns = [
    path('frontend/', ChirpList.as_view(), name='chirp_list'),
    path('frontend/front_page/', ChirpFrontPageView.as_view(), name='chirp_front_page'),
    path('frontend/<int:chirp_id>/', ChirpDetail.as_view(), name='chirp_detail'),
    path('frontend/profile/<str:username>/', ProfileDetail.as_view(), name='profile_detail'),
    path('frontend/<str:username>/profile/', UserProfileDetailView.as_view(), name='user_profile_detail'),
]
