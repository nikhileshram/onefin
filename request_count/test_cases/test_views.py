from django.test import TestCase, Client, override_settings
from django.urls import reverse, resolve
from request_count.views import RequestCountView
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
        self.headers = {
            'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'
        }

    def test_01_request_count_get(self):

        self.request_count_url = reverse('request_count:request_count_get')
        response = self.client.get(self.request_count_url, **self.headers)

        self.assertEquals(response.status_code, 200)

    def test_02_request_count_reset(self):

        self.request_count_url = reverse('request_count:request_count_reset')
        response = self.client.get(self.request_count_url, **self.headers)
        
        self.assertEquals(response.status_code, 200)
    