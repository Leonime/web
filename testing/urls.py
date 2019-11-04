from django.urls import path

from testing.views import TestingList

app_name = 'testing'

urlpatterns = [
    path('', TestingList.as_view(), name='home'),
]
