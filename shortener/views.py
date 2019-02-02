from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.views import View

from shortener.forms import SubmitUrlForm
from shortener.models import ShortURL


class ShortenerHome(View):
    form_class = SubmitUrlForm
    template_name = 'shortener/shortener_home.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Shortener",
            "form": form,
        }
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = ShortURL.objects.get_or_create(url=new_url)
            context = {
                "title": "Shortener",
                "object": obj,
                "created": created,
            }
            if created:
                self.template_name = "shortener/success.html"
            else:
                self.template_name = "shortener/exists.html"
        return render(request, self.template_name, context)


class ShortURLView(View):  # class based view
    def get(self, request, *args, **kwargs):
        short_code = kwargs['short_code']
        obj = get_object_or_404(ShortURL, short_code=short_code)
        return HttpResponseRedirect(obj.url)

    def post(self, request, *args, **kwargs):
        return HttpResponse()
