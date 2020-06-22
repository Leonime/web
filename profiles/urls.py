from django.urls import path

from profiles.views import UserProfileView

app_name = 'profiles'
urlpatterns = [
    path('profiles/create/', UserProfileView.as_view(), name='login'),
]