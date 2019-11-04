from django.views.generic import ListView

from testing.models import Testing


class TestingList(ListView):
    model = Testing
