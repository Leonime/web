from rest_framework import routers

from chirp.api.views import ChirpViewSet

chirp_router = routers.DefaultRouter()

chirp_router.register(r'chipper/chirps', ChirpViewSet)
