from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Recipe, RecipeIngredient


User = get_user_model()

class UserTestCase(TestCase):
  def setUp(self) -> None:
    self.user_a = User.objects.create_user('cfe', password='abc123')

  def test_user_pw(self):
    checked = self.user_a.check_password('abc123')
    self.assertTrue(checked)


class RecipeTestCase(TestCase):
  def setUp(self) -> None:
    self.user_a = User.objects.create_user('cfe', password='abc123')    
    self.recipe_a = Recipe.objects.create(
      user=self.user_a,
      name='Grilled Chicken'
    )
    self.recipe_b = Recipe.objects.create(
      user=self.user_a,
      name='Grilled Chicken Tacos'
    )
    self.recipe_ingredient_a = RecipeIngredient.objects.create(
      recipe=self.recipe_a,
      name='Chicken',
      quantity='1/2',
      unit='pound'
    )
    self.recipe_ingredient_b = RecipeIngredient.objects.create(
      recipe=self.recipe_a,
      name='Chicken',
      quantity='sdfssgfg',
      unit='pound'
    )

  def test_user_count(self):
    queryset = User.objects.all()
    self.assertEqual(queryset.count(), 1)

  def test_user_recipe_reverse_count(self):
    user = self.user_a
    queryset = user.recipe_set.all()  
    self.assertEqual(queryset.count(), 2)

  def test_user_recipe_forward_count(self):
    user = self.user_a
    queryset = Recipe.objects.filter(user=user)
    self.assertEqual(queryset.count(), 2)

  def test_recipe_ingredient_reverse_count(self):
    recipe = self.recipe_a
    queryset = recipe.recipeingredient_set.all()
    self.assertEqual(queryset.count(), 2)

  # -----
  
  def test_recipe_ingredient_count(self):
    recipe = self.recipe_a
    queryset = RecipeIngredient.objects.filter(recipe=recipe)
    self.assertEqual(queryset.count(), 2)

  def test_user_two_level_relation(self):
    user = self.user_a
    queryset = RecipeIngredient.objects.filter(recipe__user=user)
    self.assertEqual(queryset.count(), 2)

  def test_user_two_level_relation_reverse(self):
    user = self.user_a
    recipe_ingredient_ids = list(user.recipe_set.all().values_list('recipeingredient__id', flat=True))    
    queryset = RecipeIngredient.objects.filter(id__in=recipe_ingredient_ids)
    self.assertEqual(queryset.count(), 2)

  def test_user_two_level_via_recipes(self):
    user = self.user_a
    ids = list(user.recipe_set.all().values_list('id', flat=True))    
    queryset = RecipeIngredient.objects.filter(recipe__id__in=ids)
    self.assertEqual(queryset.count(), 2)

  def test_unit_measure_validation_error(self):
    invalid_units = ['nada', 'asdsffds']
    with self.assertRaises(ValidationError):
      for unit in invalid_units:
        ingredient = RecipeIngredient(
          name='New',
          quantity=10,
          recipe=self.recipe_a,
          unit=unit
        )
        ingredient.full_clean()

  def test_unit_measure_validation(self):
    valid_unit = 'ounce'
    ingredient = RecipeIngredient(
      name='New',
      quantity=10,
      recipe=self.recipe_a,
      unit=valid_unit
    )
    ingredient.full_clean()

  def test_quantity_as_float(self):
    self.assertIsNotNone(self.recipe_ingredient_a.quantity_as_float)
    self.assertIsNone(self.recipe_ingredient_b.quantity_as_float)