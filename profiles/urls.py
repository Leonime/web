from django.conf import settings
from django.urls import path, include

from profiles.api.routers import profiles_router
from profiles.views import UserProfileView

app_name = 'profiles'
urlpatterns = [
    path('profiles/edit/', UserProfileView.as_view(), name='user_profile'),
    path(f'{settings.API_URL}', include(profiles_router.urls)),
]
