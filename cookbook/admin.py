from django.contrib import admin

from cookbook.models import Recipe, Food, Ingredient


class IngredientInline(admin.TabularInline):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInline,)


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass
