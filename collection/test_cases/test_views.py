from django.test import TestCase, Client, override_settings
from django.urls import reverse, resolve
from collection.views import CollectionDetailView, CollectionListView
from collection.models import Collection, MovieCollection
from django.conf import settings
from django.contrib.auth.models import User
from uuid import uuid4
from rest_framework_simplejwt.tokens import RefreshToken


# remove this middleware if you want to test the api request counter functionality
@override_settings(MIDDLEWARE=[
        mw for mw in settings.MIDDLEWARE if mw != 'onefin_movie_collection.middleware.IncrementRequestApiCountMiddleware'
    ])
class TestView(TestCase):


    def setUp(self):
        self.client = Client()
        self.test_user = User.objects.create_user(username="testuser", password="testpassword")
        refresh = RefreshToken.for_user(self.test_user)
        self.access_token = str(refresh.access_token)
        id = uuid4()
        self.test_collection = Collection.objects.create(id=id, title="test", description="test", user=self.test_user)
        self.collection_uuid = self.test_collection.id
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'
        }

    def test_collection_01_post_detail_create(self):

        data = {
            "title": "test",
            "description": "test",
            "movies": [{
                "title": "movie 1 title",
                "description": "movie 1 description",
                "genre": "movie 1 genre",
                "uuid": "b53a0f7f-21d5-4833-96d5-a49b6d8e8a3a"
            }]
        }

        self.collection_list_url = reverse('collection:collection_list')
        response = self.client.post(self.collection_list_url, data, content_type='application/json', **self.headers)

        self.assertEquals(response.status_code, 201)

    def test_collection_02_get_all(self):

        self.collection_list_url = reverse('collection:collection_list')
        response = self.client.get(self.collection_list_url, **self.headers)
        
        self.assertEquals(response.status_code, 200)
    
    def test_collection_03_get_detail(self):

        self.collection_detail_url = reverse('collection:collection_detail', args=[self.collection_uuid])

        response = self.client.get(self.collection_detail_url, **self.headers)
        
        self.assertEquals(response.status_code, 200)
    
    def test_collection_04_put_detail(self):
        
        data = {
            "title": "put new title",
            "description": "put new description",
            "movies": [{
                "title": "movie 2 title",
                "description": "movie 2 description",
                "genre": "movie 2 genre",
                "uuid": "b53a0f7f-21d5-4833-96d5-a49b6d8e8a3b"
            }]
        }

        self.collection_detail_url = reverse('collection:collection_detail', args=[self.collection_uuid])
        response = self.client.put(self.collection_detail_url, data, content_type='application/json', **self.headers)

        self.assertEquals(response.status_code, 200)


    def test_collection_05_delete_detail(self):
        
        # use the collection uuid that is not in the database
        self.collection_detail_url = reverse('collection:collection_detail', args=[self.collection_uuid])

        response = self.client.delete(self.collection_detail_url, **self.headers)
        
        self.assertEquals(response.status_code, 200)