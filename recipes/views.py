from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Recipe
from .forms import RecipeForm


@login_required
def recipe_list_view(request):
  queryset = Recipe.objects.filter(user=request.user)
  context = {
    'object_list': queryset
  }
  return render(request, 'recipes/list.html', context)


@login_required
def recipe_detail_view(request, id=None):
  object = get_object_or_404(Recipe, user=request.user, id=id)
  context = {
    'object': object
  }
  return render(request, 'recipes/detail.html', context)


@login_required
def recipe_create_view(request):
  form = RecipeForm(request.POST or None)
  context = {
    'form', form
  }
  if form.is_valid():
    object = form.save(commit=False)
    object.user = request.user
    object.save()
    return redirect(object.get_absoulute_url())
  return render(request, 'recipes/create-update.html', context)


@login_required
def recipe_update_view(request, id=None):
  instance = get_object_or_404(Recipe, user=request.user, id=id)
  form = RecipeForm(request.POST or None, instance=instance)
  context = {
    'form': form,
    'object': instance
  }
  if form.is_valid():
    form.save()
    context['message'] = 'Data saved'
  return render(request, 'recipes/create-update.html', context)
