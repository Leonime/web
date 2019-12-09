from PIL import Image
from datetime import date
from django.apps import apps
from django.core.files import File
from django.test import TestCase
from io import BytesIO

from party.apps import PartyConfig
from party.models import Party, Wish, upload_to, Photo


class TestRestConfig(TestCase):
    def test_apps(self):
        self.assertEqual(PartyConfig.name, 'party')
        self.assertEqual(apps.get_app_config('party').name, 'party')


class TestParty(TestCase):
    def test_party(self):
        obj = Party(party_name='party')
        self.assertEqual(str(obj), obj.party_name)


class TestWish(TestCase):
    def test_wish(self):
        p_ob = Party(party_name='name', date_of_party=date.today())
        p_ob.save()
        w_obj = Wish(party=p_ob, w_from='from', message='a nice message')
        w_obj.save()
        self.assertEqual(str(w_obj), f'{w_obj.w_from} id:{w_obj.id}')


class TestUploadTo(TestCase):
    @staticmethod
    def get_image_file(name='test.png', ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def test_upload_to(self):
        p_ob = Party(party_name='name', date_of_party=date.today())
        p_ob.save()
        w_obj = Wish(party=p_ob, w_from='from', message='a nice message')
        w_obj.save()
        ph_obj = Photo(wish=w_obj, image=self.get_image_file())
        ph_obj.save()
        self.assertEqual(upload_to(ph_obj, ph_obj.image.name), f'photos/{ph_obj.wish_id}/{ph_obj.image.name}')
