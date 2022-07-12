from django.shortcuts import render

from articles.models import Article


def home_view(request):    
  article_queryset = Article.objects.all()
  article_object = article_queryset.order_by('?').first()  

  context = {
    'object_list': article_queryset,
    'object': article_object
  }
  
  return render(request, 'home.html', context)
