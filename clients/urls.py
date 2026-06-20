from django.urls import path

from . import views
from .views import ClientCreateAPI

urlpatterns = [
    path('create/', ClientCreateAPI.as_view()),
    path('clients/', views.client_list, name='client_list'),
    
    path(
    "client-onboarding/<int:client_id>/",
    views.client_onboarding,
    name="client_onboarding"
        ),

        path(
            "clients/<int:client_id>/onboarding/",
            views.client_onboarding,
            name="admin_client_onboarding"
        )
   
]