import random

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from chirp.forms import ChirpForm
from chirp.models import Chirp


class Index(TemplateView):
    template_name = 'chirp/index.html'


class ChirpListView(View):
    def get(self, request, *args, **kwargs):
        qs = Chirp.objects.all()
        tweets_list = [{"id": x.id, "content": x.content, "likes": random.randint(0, 122)} for x in qs]
        data = {
            "response": tweets_list
        }
        return JsonResponse(data)


class ChirpCreateView(View):
    def post(self, request, *args, **kwargs):
        form = ChirpForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            # do other form related logic
            obj.save()
            form = ChirpForm()
        return render(request, 'chirp/create_chirp.html', context={"form": form})

    def get(self, request, *args, **kwargs):
        form = ChirpForm(request.GET or None)
        return render(request, 'chirp/create_chirp.html', context={"form": form})
