from rest_framework import serializers

from party.models import Party, Wish, Photo


class PartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party
        fields = ('url', 'party_name', 'date_of_party')
        read_only_fields = ['url', ]


class WishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wish
        fields = ('url', 'party', 'w_from', 'message')
        read_only_fields = ['url', ]


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ('url', 'wish', 'image')
        read_only_fields = ['image', ]
