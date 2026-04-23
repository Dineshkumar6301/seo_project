from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),


    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/employee/', views.employee_dashboard, name='employee_dashboard'),
    path('dashboard/qa/', views.qa_dashboard, name='qa_dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('assign-services/<int:project_id>/', views.assign_services, name='assign_services'),

]