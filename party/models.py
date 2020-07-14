from django.db import models
from pprint import pprint


def upload_to(instance, filename):
    pprint(instance)
    return f'photos/{instance.wish_id}/{filename}'


class Party(models.Model):
    party_name = models.CharField(max_length=50, blank=False, null=False)
    date_of_party = models.DateField(blank=False, null=False)

    def __str__(self):
        return self.party_name


class Wish(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    w_from = models.CharField(max_length=50, blank=False, null=False)
    message = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return self.w_from + " id:" + str(self.id)


class Photo(models.Model):
    wish = models.ForeignKey(Wish, on_delete=models.CASCADE)
    image = models.ImageField(blank=False, null=False, upload_to=upload_to)
