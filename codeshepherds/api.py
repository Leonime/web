from rest_framework import routers

from chirp.api.routers import chirp_router
from party import views as party_views

router = routers.DefaultRouter()
# Party app
router.register(r'party/parties', party_views.PartyViewSet)
router.register(r'party/wishes', party_views.WishViewSet)
router.register(r'party/photos', party_views.PhotoViewSet)

router.registry.extend(chirp_router.registry)
