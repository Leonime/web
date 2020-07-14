from django.urls import path

from base.views import Error404, Error403

app_name = 'chirp'
urlpatterns = [
    path('403/', Error403.as_view(), name='403'),
    path('404/', Error404.as_view(), name='404'),
]
