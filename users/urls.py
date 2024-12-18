from django.urls import path
from .views import UserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('register/', UserView.as_view()),
    path('register/', UserView.as_view(), name='register_user'),
]