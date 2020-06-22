from rest_framework import routers

from chirp.api.routers import chirp_router
from party.api.routers import party_router

router = routers.DefaultRouter()

# Party app
router.registry.extend(party_router.registry)
# Chirp app
router.registry.extend(chirp_router.registry)
