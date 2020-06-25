from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from profiles.api.serializers import ProfileSerializer
from profiles.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    @action(methods=['POST'], detail=False, url_path='follow/(?P<username>\\w+)')
    def follow(self, request, username, *args, **kwargs):
        me = request.user
        other_user_qs = User.objects.filter(username=username)
        if me.username == username:
            my_followers = me.profile.followers.all()
            return Response({"count": my_followers.count()}, status=200)
        if not other_user_qs.exists():
            return Response({}, status=404)
        other = other_user_qs.first()
        profile = other.profile
        data = request.data or {}
        follow_action = data.get("action")
        if follow_action == "follow":
            profile.followers.add(me)
        elif follow_action == "unfollow":
            profile.followers.remove(me)
        else:
            pass
        current_followers_qs = profile.followers.all()
        return Response({"count": current_followers_qs.count()}, status=200)
