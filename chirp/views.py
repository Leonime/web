import random

from django.conf import settings
from django.conf.global_settings import ALLOWED_HOSTS
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views import View
from django.views.generic import TemplateView

from chirp.forms import ChirpForm
from chirp.models import Chirp


class Index(TemplateView):
    template_name = 'chirp/index.html'


class ChirpListView(View):
    def get(self, request, *args, **kwargs):
        qs = Chirp.objects.all()
        tweets_list = [x.serialize() for x in qs]
        data = {
            "is_user": False,
            "response": tweets_list
        }
        return JsonResponse(data)


class ChirpCreateView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.is_ajax():
                return JsonResponse({}, status=401)
            return redirect(settings.LOGIN_URL)
        form = ChirpForm(request.POST or None)
        next_url = request.POST.get("next") or None
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user or None
            obj.save()
            if request.is_ajax():
                return JsonResponse(obj.serialize(), status=201)
            if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
                return redirect(next_url)
            form = ChirpForm()

        if form.errors:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
        return render(request, 'chirp/create_chirp.html', context={"form": form})

    def get(self, request, *args, **kwargs):
        form = ChirpForm(request.GET or None)
        return render(request, 'chirp/create_chirp.html', context={"form": form})
