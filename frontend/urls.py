from django.urls import path

from frontend.views import Index

app_name = 'frontend'
urlpatterns = [
    path('frontend/', Index.as_view(), name='index'),
]
