from rest_framework import routers

from profiles.api.views import ProfileViewSet

profiles_router = routers.DefaultRouter()

profiles_router.register(r'profiles/profile', ProfileViewSet)
