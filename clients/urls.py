from django.urls import path

from . import views
from .views import ClientCreateAPI

urlpatterns = [
    path('create/', ClientCreateAPI.as_view()),
    path('clients/', views.client_list, name='client_list'),
    
]