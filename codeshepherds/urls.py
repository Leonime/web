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
from rest_framework.documentation import include_docs_urls

from codeshepherds.routers import router
from home.views import Index

urlpatterns = [
    # Admin urls
    path('admin/', admin.site.urls),

    # Accounts app urls
    path('', include('accounts.urls', namespace='accounts')),

    # Chat app urls
    path('chat/', include('chat.urls', namespace='chat')),

    # Chipper app urls
    path('', include('chirp.urls', namespace='chipper')),

    # Frontend app urls
    path('', include('frontend.urls', namespace='frontend')),

    # Home urls
    path('', Index.as_view(), name='index'),
    path('s/', include('shortener.urls', namespace='shortener')),

    # party App Urls
    path('party/', include(router.urls)),

    # Profile app urls
    path('', include('profiles.urls', namespace='profiles')),

    # REST API urls
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/docs/', include_docs_urls(title='API Docs', public=False)),
    path(f'{settings.API_URL}', include(router.urls)),

    # Testing urls
    path('test/', include('testing.urls', namespace='testing')),

    # Thumbnailer
    path('thumbnailer/', include('thumbnailer.urls', namespace='thumbnailer')),

    # Cookbook
    path('cookbook/', include('cookbook.urls', namespace='cookbook'))
]

urlpatterns += static(getattr(settings, "STATIC_URL", '/static/'),
                      document_root=getattr(settings, "STATIC_ROOT", 'static'))
urlpatterns += static(getattr(settings, "MEDIA_URL", '/media/'),
                      document_root=getattr(settings, "MEDIA_ROOT", 'media'))
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
