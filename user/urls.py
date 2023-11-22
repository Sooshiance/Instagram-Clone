from django.urls import path

from .views import *


urlpatterns = [
    path('', CustomTokenObtainPairView, name='LOGIN'),
]
