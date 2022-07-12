from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm


def article_serch_view(request):
  query_dict = request.GET
  query = query_dict.get('q')

  try:
    article_object = Article.objects.get(id=query)
  except:
    article_object = None
    
  context = {
    'object': article_object
  }

  return render(request, 'articles/search.html', context)


@login_required
def article_create_view(request):     
  form = ArticleForm(request.POST or None)
  context = {
    'form': form
  }  

  if form.is_valid():  
    article_object = form.save()      
    context['form'] = ArticleForm()
    # context['object'] = article_object  

  return render(request, 'articles/create.html', context)


def article_detail_view(request, id=None):      
  article_object = None
  if id is not None:
    article_object = Article.objects.get(id=id)

  context = {
    'object': article_object
  }

  return render(request, 'articles/detail.html', context)
