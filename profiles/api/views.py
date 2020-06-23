from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from profiles.api.serializers import ProfileSerializer
from profiles.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
