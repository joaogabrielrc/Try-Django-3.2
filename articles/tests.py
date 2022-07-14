from django.test import TestCase
from django.utils.text import slugify

from .models import Article
from .utils import slugify_instance_title


class ArticleTestCase(TestCase):
  number_of_articles = 5_000

  def setUp(self) -> None:
    for i in range(0, self.number_of_articles):
      Article.objects.create(title='Hello World', content='something else')
  
  def test_queryset_exists(self) -> None:
    queryset = Article.objects.all()
    self.assertTrue(queryset.exists())

  def test_queryset_count(self) -> None:
    queryset = Article.objects.all()
    self.assertEqual(queryset.count(), self.number_of_articles)

  def test_hello_world_slug(self):
    object = Article.objects.all().order_by('id').first()
    slugified_title = slugify(object.title)
    self.assertEqual(object.slug, slugified_title)

  def test_hello_world_unique_slug(self):
    queryset = Article.objects.exclude(slug__iexact='hello-world')
    for object in queryset:
      slugified_title = slugify(object.title) 
      self.assertNotEqual(object.slug, slugified_title)

  def test_slugify_instance_title(self):
    object = Article.objects.all().last()
    slug_list = []
    for i in range(0, 25):
      instance = slugify_instance_title(object, save=False)
      slug_list.append(instance.slug)
    unique_slug_list = list(set(slug_list))
    self.assertEqual(len(unique_slug_list), len(slug_list))

  def test_slugify_instance_title_redux(self):
    slug_list = Article.objects.all().values_list('slug', flat=True)
    unique_slug_list = list(set(slug_list))
    self.assertEqual(len(unique_slug_list), len(slug_list))
