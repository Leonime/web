from django.urls import path

from base.views import Error404, Error500

app_name = 'chirp'
urlpatterns = [
    path('404/', Error404.as_view(), name='404'),
    path('500/', Error500.as_view(), name='500'),
]
