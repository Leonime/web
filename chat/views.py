import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View


class Index(LoginRequiredMixin, View):
    template_name = 'chat/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


class Room(LoginRequiredMixin, View):
    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):
        room_name = kwargs['room_name']
        context = {
            'room_name_json': mark_safe(json.dumps(room_name))
        }
        return render(request, self.template_name, context)
