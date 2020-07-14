from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from rest_framework import status


class ErrorBase(TemplateView):
    template_name = 'base/error_page.html'


class Error404(ErrorBase):
    def get(self, request, *args, **kwargs):
        status_code = str()
        for char in str(status.HTTP_404_NOT_FOUND):
            status_code += f'<span>{char}</span>'
        context = dict(
            tittle='Page not found',
            error='Page not found',
            status=mark_safe(status_code),
            description='We’re sorry, but the requested page could not be found.',
        )
        return render(request, self.template_name, context, status=status.HTTP_404_NOT_FOUND)


class Error500(ErrorBase):
    def get(self, request, *args, **kwargs):
        status_code = str()
        for char in str(status.HTTP_500_INTERNAL_SERVER_ERROR):
            status_code += f'<span>{char}</span>'
        context = dict(
            tittle='Server error (500)',
            error='Server error (500)',
            status=mark_safe(status_code),
            description='There’s been an error. It’s been reported to the site administrators via email and should be'
                        ' fixed shortly. Thanks for your patience.',
        )
        return render(request, self.template_name, context, status=status.HTTP_404_NOT_FOUND)
