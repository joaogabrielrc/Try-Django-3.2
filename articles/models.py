from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify


class Article(models.Model):
  title = models.CharField(max_length=120)
  slug = models.SlugField(blank=True, null=True)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):    
    super().save(*args, **kwargs)


def slugify_instance_title(instance, save=False):
  slug = slugify(instance.title)
  queryset = Article.objects.filter(slug=slug).exclude(id=instance.id)
  if queryset.exists():
    slug = f'{slug}-{queryset.count() + 1}'
  instance.slug = slug
  if save:
    instance.save()  


def article_pre_save(sender, instance, *args, **kwargs):
  print('pre_save')  
  if instance.slug is None:
    slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
  print('post_save')  
  if created:
    slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)
