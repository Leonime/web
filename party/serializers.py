from party.models import Party, Wish, Photo
from rest_framework import serializers
        
class PartySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Party
        fields = ('url', 'party_name', 'date_of_party')
        readonly_fields = ('url')
        
    
class WishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wish
        fields = ('url', 'party', 'w_from', 'message')
        readonly_fields = ('url')
        
        
class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ('url', 'wish', 'image')
        readonly_fields = ('image')