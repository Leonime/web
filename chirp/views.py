import logging

from django.conf import settings
from django.conf.global_settings import ALLOWED_HOSTS
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views import View
from django.views.generic import TemplateView
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from chirp.forms import ChirpForm
from chirp.models import Chirp
from chirp.serializers import ChirpSerializer, ChirpActionSerializer

logger = logging.getLogger(__name__)


class Index(TemplateView):
    template_name = 'chirp/index.html'


class ChirpCreateView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        form = ChirpForm(request.POST or None)
        next_url = request.POST.get("next") or None
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user or None
            obj.save()
            if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
                return redirect(next_url)
            form = ChirpForm()

        if form.errors:
            if request.is_ajax():
                return JsonResponse(form.errors, status=400)
        return render(request, 'chirp/create_chirp.html', context={"form": form})

    def get(self, request, *args, **kwargs):
        form = ChirpForm(request.GET or None)
        return render(request, 'chirp/create_chirp.html', context={"form": form})


class ChirpViewSet(viewsets.ModelViewSet):
    queryset = Chirp.objects.all()
    serializer_class = ChirpSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]

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
