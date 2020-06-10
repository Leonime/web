from django.conf import settings
from rest_framework import serializers
from chirp.models import Chirp


class ChirpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chirp
        fields = ['id', 'content']
