from rest_framework import routers

from party import views as party_views
from chirp import views as chipper_views

router = routers.DefaultRouter()
# Party app
router.register(r'party/parties', party_views.PartyViewSet)
router.register(r'party/wishes', party_views.WishViewSet)
router.register(r'party/photos', party_views.PhotoViewSet)

router.register(r'chipper/chirps', chipper_views.ChirpViewSet)
