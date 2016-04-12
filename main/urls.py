from django.conf.urls import patterns, url

from main.views import Welcome

urlpatterns = patterns(
    'main.views',
    url(r'^', Welcome.as_view(), name='welcome'),
)