from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from chirp.models import Chirp


class Index(TemplateView):
    template_name = 'chirp/index.html'


class ChirpListView(View):
    def get(self, request, *args, **kwargs):
        qs = Chirp.objects.all()
        tweets_list = [{"id": x.id, "content": x.content} for x in qs]
        data = {
            "response": tweets_list
        }
        return JsonResponse(data)
