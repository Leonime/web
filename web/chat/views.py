from django.shortcuts import render
from django.views import View


class Index(View):
    template_name = 'chat/'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
