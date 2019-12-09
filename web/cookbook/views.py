from django.shortcuts import render
from django.views import View

from cookbook.services import get_recipes_with_cache as get_recipes


class RecipesHome(View):
    template_name = 'cookbook/recipes.html'

    def get(self, request, *args, **kwargs):
        context = {
            "recipes": get_recipes()
        }
        return render(request, self.template_name, context)
