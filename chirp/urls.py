from django.urls import path

from chirp.views import Index

app_name = 'chirp'
urlpatterns = [
    path('', Index.as_view(), name='index'),
]
