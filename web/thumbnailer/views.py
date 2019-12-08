import os

from celery import current_app
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from thumbnailer.forms import FileUploadForm
from thumbnailer.tasks import make_thumbnails


class HomeView(View):
    form_class = FileUploadForm
    template_name = 'thumbnailer/home.html'

    def get(self, request):
        form = self.form_class()
        context = {
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        context = {
            "form": form
        }

        if form.is_valid():
            file_path = os.path.join(settings.IMAGES_DIR, request.FILES['image_file'].name)

            with open(file_path, 'wb+') as fp:
                for chunk in request.FILES['image_file']:
                    fp.write(chunk)

            task = make_thumbnails.delay(file_path, thumbnails=[(128, 128)])

            context = {
                "form": form,
                'task_id': task.id,
                'task_status': task.status
            }

            return render(request, self.template_name, context)

        return render(request, self.template_name, context)


class TaskView(View):
    def get(self, request, task_id):
        task = current_app.AsyncResult(task_id)
        response_data = {'task_status': task.status, 'task_id': task.id}

        if task.status == 'SUCCESS':
            response_data['results'] = task.get()

        return JsonResponse(response_data)
