from django.urls import path
from .views import RegisterAPI, LoginAPI
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('profile/', views.profile_view, name='profile_view'),
]
