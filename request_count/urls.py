from django.urls import path
from .views import RequestCountView

urlpatterns = [
    path('', RequestCountView.as_view(), name='request_count_get'),
    path('reset/', RequestCountView.as_view(), name='request_count_reset'),
]