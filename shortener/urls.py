from django.urls import path, register_converter

from shortener.converters import ShortCodeConverter
from shortener.views import ShortURLView, ShortenerHome

register_converter(ShortCodeConverter, 'code_converter')

urlpatterns = [
    path('', ShortenerHome.as_view(), name='home'),
    path('<code_converter:short_code>/', ShortURLView.as_view(), name='short_code'),
]
