from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Article
from .forms import ArticleForm


def article_serch_view(request):
  query = request.GET.get('q')    
  queryset = Article.objects.search(query)
    
  context = {
    'object_list': queryset
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
    # return redirect('article-detail', slug=article_object.slug)
    return redirect(article_object.get_absolute_url())
    # context['object'] = article_object  

  return render(request, 'articles/create.html', context)


def article_detail_view(request, slug=None):      
  article_object = None
  if slug is not None:
    try:
      article_object = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
      raise Http404
    except Article.MultipleObjectsReturned:
      article_object = Article.objects.filter(slug=slug).first()
    except:
      raise Http404

  context = {
    'object': article_object
  }

  return render(request, 'articles/detail.html', context)
