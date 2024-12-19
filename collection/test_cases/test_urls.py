from django.test import SimpleTestCase
from django.urls import reverse, resolve
from collection.views import CollectionDetailView, CollectionListView

# Create your tests here.
class CollectionTest(SimpleTestCase):

    def test_collection_detail_url_resolves(self):
        url = reverse('collection:collection_detail', args=['123e4567-e89b-12d3-a456-426614174000'])
        self.assertEquals(resolve(url).func.view_class, CollectionDetailView)

    def test_collection_list_url_resolves(self):
        url = reverse('collection:collection_list')
        self.assertEquals(resolve(url).func.view_class, CollectionListView)