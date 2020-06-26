from django.urls import path

from testing.views import TestingList, TestProfileTemplate

app_name = 'testing'

urlpatterns = [
    path('', TestingList.as_view(), name='home'),
    path('testing/profile', TestProfileTemplate.as_view(), name='test_profile')
]
