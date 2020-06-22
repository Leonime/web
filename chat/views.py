import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View


@login_required
class Index(View):
    template_name = 'chat/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)


@login_required
class Room(View):
    template_name = 'chat/room.html'

    def get(self, request, *args, **kwargs):
        room_name = kwargs['room_name']
        context = {
            'room_name_json': mark_safe(json.dumps(room_name))
        }
        return render(request, self.template_name, context)
