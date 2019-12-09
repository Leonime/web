from django.urls import path

from cookbook.views import RecipesHome

app_name = 'cookbook'
urlpatterns = [
    path('', RecipesHome.as_view()),
]
