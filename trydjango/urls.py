from django.contrib import admin
from django.urls import path

from accounts.views import (
    login_view,
    logout_view,
    register_view
)
from .views import home_view
from articles.views import (
  article_serch_view,
  article_create_view,
  article_detail_view
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    path('', home_view),
    
    path('articles/', article_serch_view),
    path('articles/create/', article_create_view, name='article-create'),
    path('articles/<slug:slug>/', article_detail_view, name='article-detail')
]
