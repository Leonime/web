from django.views.generic import ListView, TemplateView

from testing.models import Testing


class TestingList(ListView):
    model = Testing


class TestProfileTemplate(TemplateView):
    template_name = 'testing/profile.html'
