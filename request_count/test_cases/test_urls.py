from django.test import SimpleTestCase
from django.urls import reverse, resolve
from request_count.views import RequestCountView

# Create your tests here.
class RequestCountTest(SimpleTestCase):

    def test_request_count_get_url_resolves(self):
        url = reverse('request_count:request_count_get')
        self.assertEquals(resolve(url).func.view_class, RequestCountView)

    def test_request_count_reset_url_resolves(self):
        url = reverse('request_count:request_count_reset')
        self.assertEquals(resolve(url).func.view_class, RequestCountView)