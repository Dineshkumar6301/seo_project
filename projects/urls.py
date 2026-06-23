from django.urls import path
from . import views
from .views import ProjectCreateAPI, RemoveUserFromService


urlpatterns = [
    path('', views.project_list, name='project_list'),  
    path('create/', views.project_create, name='project_create'),  
    path('api/create/', ProjectCreateAPI.as_view(), name='api_project_create'),
    path('project-dashboard/', views.project_dashboard, name='project_dashboard'),
    path('add-service/', views.add_service, name='add_service'),
    path('remove-user/', RemoveUserFromService.as_view(), name='remove_user'),
    path('rank/', views.rank_page, name='rank'),

path(
    'api/rank/',
    views.get_project_rank_data,
    name='rank_details'
),

path(
    'api/check-rank/',
    views.check_keyword_rank,
    name='check_keyword_rank'
),
path(
    'api/project-ranks/',
    views.project_rank_results,
    name='project_rank_results'
),
# urls.py
path(
        "api/run-rank-check/",
        views.run_rank_check,
        name="run_rank_check"
    ),
]