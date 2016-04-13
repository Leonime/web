from django.conf.urls import url

from main.views import Welcome

urlpatterns = [
    url(r'^', Welcome.as_view(), name='welcome'),
]
