from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from chirp.api.serializers import ChirpSerializer, ChirpActionSerializer
from chirp.models import Chirp
from chirp.views import logger
from codeshepherds.api.paginators import RelativePageNumberPagination


class ChirpViewSet(viewsets.ModelViewSet):
    queryset = Chirp.objects.all()
    serializer_class = ChirpSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = RelativePageNumberPagination

    def perform_create(self, serializer, *args, **kwargs):
        if 'user' in kwargs:
            serializer.save(user=kwargs['user'])
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def like_action(self, request, pk=None):
        try:
            chirp = self.get_object()
            serializer = ChirpActionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                data = serializer.validated_data
                like_action = data.get("action")
                content = data.get("content")

                if like_action == "chirp":
                    chirp.likes.add(request.user)
                    serializer = ChirpSerializer(chirp)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                elif like_action == "unchirp":
                    chirp.likes.remove(request.user)
                elif like_action == "rechirp":
                    new_chirp = Chirp.objects.create(
                        user=request.user,
                        parent=chirp,
                        content=content,
                    )
                    serializer = ChirpSerializer(new_chirp)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data, status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(e)

    @action(methods=['GET'], detail=False)
    def feed(self, request, *args, **kwargs):
        user = request.user
        queryset = Chirp.objects.feed(user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)
