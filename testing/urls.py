from django.urls import path

from testing.views import TestingList, TestProfileTemplate, GalleryView

app_name = 'testing'

urlpatterns = [
    path('testing', TestingList.as_view(), name='home'),
    path('testing/profile', TestProfileTemplate.as_view(), name='test_profile'),
    path('testing/gallery', GalleryView.as_view(), name='gallery')
]
