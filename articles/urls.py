from django.urls import path

from .views import (
  article_serch_view,
  article_create_view,
  article_detail_view
)


urlpatterns = [
  path('', article_serch_view),
  path('create/', article_create_view),
  path('<slug:slug>/', article_detail_view)
]