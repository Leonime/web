from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from ipware import get_client_ip

from analytics.models import SURLAnalytics
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
        g = GeoIP2()
        client_ip, is_routable = get_client_ip(request)
        geolocation = {}
        print(client_ip)

        if client_ip is None:
            # Unable to get the client's IP address
            geolocation['ipv4'] = ''
            geolocation['city'] = ''
            geolocation['country_code'] = ''
            geolocation['country'] = ''
            geolocation['found'] = False
            pass
        else:
            # We got the client's IP address
            if is_routable:
                # The client's IP address is publicly routable on the Internet
                geolocation['ipv4'] = client_ip
                city = g.city(client_ip)
                geolocation['city'] = city['city']
                geolocation['country_code'] = city['country_code']
                geolocation['country'] = city['country_name']
                geolocation['found'] = True
                pass
            else:
                # The client's IP address is private
                geolocation['ipv4'] = client_ip
                geolocation['city'] = ''
                geolocation['country_code'] = ''
                geolocation['country'] = ''
                geolocation['found'] = None
                pass

        SURLAnalytics.objects.create_event(obj, geolocation)
        return HttpResponseRedirect(obj.url)
