from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView

from testing.forms import GalleryForm
from testing.models import Testing, Gallery


class TestingList(ListView):
    model = Testing


class TestProfileTemplate(TemplateView):
    template_name = 'testing/profile.html'


class GalleryView(FormView):
    form_class = GalleryForm
    template_name = 'testing/galllery.html'
    success_url = '/testing/gallery'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        gallery = Gallery.objects.all()
        context = {
            'gallery': gallery,
            'form': self.form_class
        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        gallery = Gallery.objects.all()
        context = {
            'gallery': gallery,
            'form': self.form_class
        }
        return render(request, self.template_name, context)
