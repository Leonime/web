from django.shortcuts import render
from rest_framework import viewsets
from party.serializers import PartySerializer, WishSerializer, PhotoSerializer
from party.models import Party, Wish, Photo
from rest_framework.decorators import parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

class PartyViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer
    
    
class WishViewSet(viewsets.ModelViewSet):
    queryset = Wish.objects.all()
    serializer_class = WishSerializer
    

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    
    @parser_classes((FormParser, MultiPartParser,))
    def create(self, request, *args, **kwargs):
        if 'upload' in request.data:
            upload =request.data['upload']
            photo = Photo()
            photo.wish_id = request.data['id'].strip('/').split('/').pop()
            photo.image = request.data['upload']
            photo.save()
            
            
            #user_profile = self.get_object()
            ##user_profile.image.delete()

            #upload = request.data['upload']

            #user_profile.image.save(upload.name, upload)

            return Response(status=HTTP_201_CREATED, headers={'Location': photo.image.url})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        
    
    def destroy (self, request, pk=None):
        print(pk)
        photo = self.get_object()
        photo.image.delete()
        return super().destroy(request, pk)
