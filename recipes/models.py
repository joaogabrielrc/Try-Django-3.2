import pint

from django.conf import settings
from django.db import models
from django.urls import reverse

from recipes.utils import number_str_to_float

from .validators import validate_unit_of_measure


class Recipe(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  name = models.CharField(max_length=220)
  description = models.TextField(blank=True, null=True)
  directions = models.TextField(blank=True, null=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)

  def get_absoulute_url(self):
    return reverse('recipes:detail', kwargs={'id', self.id})


class RecipeIngredient(models.Model):
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
  name = models.CharField(max_length=220)
  description = models.TextField(blank=True, null=True)
  quantity = models.CharField(max_length=50)
  quantity_as_float = models.FloatField(blank=True, null=True)
  unit = models.CharField(max_length=50, validators=[validate_unit_of_measure])
  directions = models.TextField(blank=True, null=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  active = models.BooleanField(default=True)

  def get_absoulute_url(self):
    return self.recipe.get_absoulute_url()

  def convert_to_system(self, system='mks'):
    if self.quantity_as_float is None:
      return None
    ureg = pint.UnitRegistry(system=system)
    measurement = self.quantity_as_float * ureg[self.unit]
    return measurement

  def as_mks(self):
    # meter, kilogram, second
    measurement = self.convert_to_system(system='mks')
    return measurement.to_base_units()
  
  def as_imperial(self):
    # miles, pounds, seconds
    measurement = self.convert_to_system(system='imperial')
    return measurement.to_base_units()

  def save(self, *args, **kwargs):
    quantity_as_float, quantity_as_float_success = number_str_to_float(self.quantity)
    if quantity_as_float_success:
      self.quantity_as_float = quantity_as_float
    else:
      self.quantity_as_float = None
    super().save(*args, **kwargs)
