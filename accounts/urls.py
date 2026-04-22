from django.urls import path
from .views import RegisterAPI, LoginAPI
from . import views

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),
    path('profile/', views.profile_view, name='profile_view'),
]
