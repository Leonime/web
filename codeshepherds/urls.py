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
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from rest_framework import routers
from party import views
from settings import production
from home.views import Index

router = routers.DefaultRouter()
router.register(r'parties', views.PartyViewSet)
router.register(r'wishes', views.WishViewSet)
router.register(r'photos', views.PhotoViewSet)


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # Home urls
    url(r'^$', Index.as_view(), name='index'),

    # party App Urls
    url(r'^party/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(production.MEDIA_URL, document_root=production.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
