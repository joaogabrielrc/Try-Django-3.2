from django.contrib import admin

from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
  list_display = ['id', 'title']
  list_display_links = ['title']
  search_fields = ['id', 'title']
