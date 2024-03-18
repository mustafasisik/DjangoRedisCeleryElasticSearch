from django.urls import path
from .views import *

app_name = 'app'
urlpatterns = [
    # textgen
    path('search/', SearchAPIView.as_view(), name='search'),
    path('user/register/', UserRegistrationAPIView.as_view()),
    path('user/login/', UserLoginAPIView.as_view()),
    path('user/', UserViewAPI.as_view()),
]