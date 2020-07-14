from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from profiles.api.serializers import ProfileSerializer
from profiles.models import Profile


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_queryset(self):
        return Profile.objects.all().prefetch_related(
            'user',
            'followers',
            'followers__following'
        ).annotate(Count('followers', distinct=True))

    @action(methods=['POST'], detail=False, url_path='follow/(?P<username>\\w+)')
    def follow(self, request, username, *args, **kwargs):
        me = request.user
        other_user_qs = User.objects.filter(username=username)
        if me.username == username:
            data = ProfileSerializer(instance=me.profile, context={"request": request})
            return Response(data.data, status=200)
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
        data = ProfileSerializer(instance=profile, context={"request": request})
        return Response(data.data, status=200)

    @action(methods=['GET'], detail=False, url_path='profile/(?P<username>\\w+)')
    def profile_username(self, request, username, *args, **kwargs):
        qs = Profile.objects.filter(user__username=username).prefetch_related(
            'user',
            'user__following',
            'user__chirp_set',
            'followers',
            'followers__following'
        ).annotate(Count('followers', distinct=True))\
            .annotate(Count('user__following', distinct=True))\
            .annotate(Count('user__chirp', distinct=True))
        if not qs.exists():
            return Response({"detail": "User not found"}, status=404)
        profile_obj = qs.first()
        data = ProfileSerializer(instance=profile_obj, context={"request": request})
        return Response(data.data, status=status.HTTP_200_OK)
