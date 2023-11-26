from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import *


urlpatterns = [
    path("", UserLoginAPIView.as_view(), name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
]
