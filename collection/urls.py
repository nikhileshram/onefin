from django.urls import path
from .views import CollectionDetailView, CollectionListView

urlpatterns = [
    path('', CollectionListView.as_view(), name='collection_list'),
    path('<uuid:collection_uuid>/', CollectionDetailView.as_view(), name='collection_detail'),
]