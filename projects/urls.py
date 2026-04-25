from django.urls import path
from . import views
from .views import ProjectCreateAPI, RemoveUserFromService


urlpatterns = [

    # =========================
    # 🔷 UI ROUTES
    # =========================
    path('', views.project_list, name='project_list'),  
    path('create/', views.project_create, name='project_create'),  

    # =========================
    # 🔷 API ROUTES
    # =========================
    path('api/create/', ProjectCreateAPI.as_view(), name='api_project_create'),
    path('project-dashboard/', views.project_dashboard, name='project_dashboard'),
    path('add-service/', views.add_service, name='add_service'),
    path('remove-user/', RemoveUserFromService.as_view(), name='remove_user')
]