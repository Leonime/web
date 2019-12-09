from django.urls import path

from thumbnailer.views import HomeView, TaskView

app_name = 'thumbnailer'
urlpatterns = [
  path('', HomeView.as_view(), name='home'),
  path('task/<str:task_id>/', TaskView.as_view(), name='task'),
]
