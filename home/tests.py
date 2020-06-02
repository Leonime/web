from django.apps import apps
from django.test import TestCase

from home.apps import HomeConfig


class TestHomeConfig(TestCase):
    def test_apps(self):
        self.assertEqual(HomeConfig.name, 'home')
        self.assertEqual(apps.get_app_config('home').name, 'home')
