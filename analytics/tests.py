from django.apps import apps
from django.shortcuts import get_object_or_404
from django.test import TestCase

from analytics.apps import AnalyticsConfig
from analytics.management.commands.update_geoip import Command
from analytics.models import SURLAnalytics, GeoLocation
from shortener.models import ShortURL


class TestAnalyticsConfig(TestCase):
    def test_apps(self):
        self.assertEqual(AnalyticsConfig.name, 'analytics')
        self.assertEqual(apps.get_app_config('analytics').name, 'analytics')


class TestCommand(TestCase):
    def test_handle(self):
        obj = Command()
        self.assertTrue(obj.handle())


class TestSURLAnalyticsManager(TestCase):
    def test_create_event(self):
        short_url = ShortURL(url='www.google.com')
        short_url.save()
        obj = get_object_or_404(ShortURL, short_code=short_url.short_code)

        geolocation = {'ipv4': '', 'city': '', 'country_code': '', 'country': '', 'found': False}

        self.assertEqual(SURLAnalytics.objects.create_event(obj, geolocation), 1)
        self.assertIsNone(SURLAnalytics.objects.create_event(None, geolocation))


class TestSURLAnalytics(TestCase):
    def test_string_representation(self):
        obj = SURLAnalytics()
        self.assertEqual(str(obj), str(obj.count))


class TestGeoLocation(TestCase):
    def test_string_representation(self):
        obj = GeoLocation(country='US')
        self.assertEqual(str(obj), obj.country)
