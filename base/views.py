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


class Error403(ErrorBase):
    def dispatch(self, request, *args, **kwargs):
        return super(Error403, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        status_code = str()
        for char in str(status.HTTP_403_FORBIDDEN):
            status_code += f'<span>{char}</span>'
        context = dict(
            tittle='Permission denied',
            error='Access denied',
            status=mark_safe(status_code),
            description='You don’t have permission to access this area.',
        )
        return render(request, self.template_name, context, status=status.HTTP_403_FORBIDDEN)
