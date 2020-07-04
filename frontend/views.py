from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response

from profiles.api.serializers import ProfileSerializer
from profiles.models import Profile


class Index(TemplateView):
    template_name = 'react/chirp/index.html'


class ChirpList(TemplateView):
    template_name = 'react/chirp/list.html'

    def get(self, request, *args, **kwargs):
        context = {
            'user': request.user
        }
        return render(request, self.template_name, context)


class ChirpFrontPageView(TemplateView):
    template_name = 'react/chirp/front_page.html'


class ChirpDetail(TemplateView):
    template_name = 'react/chirp/detail.html'

    def get(self, request, *args, **kwargs):
        super(ChirpDetail, self).get(request, *args, **kwargs)
        chirp_id = self.kwargs.get('chirp_id' or None)
        context = {"chirp_id": chirp_id}
        return render(request, self.template_name, context)


class ProfileDetail(TemplateView):
    template_name = 'react/profiles/detail.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username' or None)
        qs = Profile.objects.filter(user__username=username)
        if not qs.exists():
            raise Http404
        profile_obj = qs.first()
        is_following = False
        if request.user.is_authenticated:
            user = request.user
            is_following = user in profile_obj.followers.all()
        context = {
            "username": username,
            "profile": profile_obj,
            "is_following": is_following
        }
        return render(request, self.template_name, context)
