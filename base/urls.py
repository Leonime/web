from django.urls import path

from base.views import Error404

app_name = 'chirp'
urlpatterns = [
    path('404/', Error404.as_view(), name='404'),
]
