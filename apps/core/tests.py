from django.test import TestCase, Client
from django.urls import reverse
from apps.forum.models import Category
from apps.core.views import FrontpageView
from factory.django import DjangoModelFactory

# Define a factory for the Category model
class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

class FrontpageViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_with_categories(self):
        # Arrange
        categories = [CategoryFactory(threads=True) for _ in range(5)]
        self._extracted_from_test_get_with_no_threads_4(5)

    def test_get_with_no_categories(self):
        self._extracted_from_test_get_with_no_threads_4(0)

    def test_get_with_many_categories(self):
        # Arrange
        categories = [CategoryFactory(threads=True) for _ in range(1000)]
        self._extracted_from_test_get_with_no_threads_4(1000)

    def test_get_with_no_threads(self):
        # Arrange
        categories = [CategoryFactory(threads=False) for _ in range(5)]
        self._extracted_from_test_get_with_no_threads_4(0)

    # TODO Rename this here and in `test_get_with_categories`, `test_get_with_no_categories`, `test_get_with_many_categories` and `test_get_with_no_threads`
    def _extracted_from_test_get_with_no_threads_4(self, arg0):
        url = reverse('frontpage')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['categories']), arg0)
