from rest_framework import routers

from party.api.views import PhotoViewSet, WishViewSet, PartyViewSet

party_router = routers.DefaultRouter()

party_router.register(r'party/parties', PartyViewSet)
party_router.register(r'party/wishes', WishViewSet)
party_router.register(r'party/photos', PhotoViewSet)
