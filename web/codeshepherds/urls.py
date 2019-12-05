"""codeshepherds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from rest_framework import routers

from home.views import Index
from party import views

router = routers.DefaultRouter()
router.register(r'parties', views.PartyViewSet)
router.register(r'wishes', views.WishViewSet)
router.register(r'photos', views.PhotoViewSet)


urlpatterns = [
    # Admin urls
    path('admin/', admin.site.urls),

    # Home urls
    path('', Index.as_view(), name='index'),
    path('s/', include('shortener.urls', namespace='shortener')),

    # party App Urls
    path('party/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Testing urls
    path('test/', include('testing.urls', namespace='testing')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(getattr(settings, "MEDIA_URL", '/media/'), document_root=getattr(settings, "MEDIA_ROOT", 'media'))
urlpatterns += staticfiles_urlpatterns()
