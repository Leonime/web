from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):
    template_name = 'react/chirp/index.html'


class ChirpDetail(TemplateView):
    template_name = 'react/chirp/detail.html'

    def get(self, request, *args, **kwargs):
        super(ChirpDetail, self).get(request, *args, **kwargs)
        chirp_id = self.kwargs.get('chirp_id' or None)
        context = {"chirp_id": chirp_id}
        return render(request, self.template_name, context)
