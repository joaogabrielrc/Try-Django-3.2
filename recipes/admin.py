from django.contrib import admin

from .models import Recipe, RecipeIngredient


class RecipeIngredientInLine(admin.StackedInline):
  model = RecipeIngredient
  extra = 0
  # fields = ['name', 'quantity', 'unit', 'directions']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
  inlines = [RecipeIngredientInLine]
  list_display = ['id', 'name', 'user']
  list_display_links = ['name']
  readonly_fields = ['timestamp', 'updated']
  raw_id_fields = ['user']
