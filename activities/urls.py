from django.urls import path

from activities.api.assignedwork import AssignedWorkAPI
from activities.api.assign_service import AssignServiceAPI
from activities.api.service_module import ServiceModulesAPI

from . import views
from .views import SaveActivityAPI
from activities.api.assignment import DeleteAssignmentAPI   

# API imports (keep only what you need)
from activities.api.create import ActivityCreateAPI
from activities.api.list import ActivityListAPI
from activities.api.update import ActivityUpdateAPI
from activities.api.delete import ActivityDeleteAPI
from activities.api.approval import ActivityApprovalAPI
from activities.api.daily_reports import DailyReportAPI
from activities.api.project_report import ProjectReportAPI
from activities.api.dashboard import ClientDashboardAPI
# activities/urls.py
from activities.api.checklist import ChecklistItemsAPI
from django.urls import path
from activities.api.today import TodayActivityAPI
from activities.api.upsert import ActivityUpsertAPI
from activities.api.export import ExportExcelAPI
from activities.api.project_services import ProjectServicesAPI
from activities.api.forget_password import ForgotPasswordAPI
from activities.api.reset_password import ResetPasswordAPI
from activities.api.activity_detail import ActivityDetailAPI
from activities.api.service_module import ServiceModulesAPI
from activities.api.taskfiled import TaskFieldsAPI

urlpatterns = [


    path('daily/', views.activity_daily, name='activity_daily'),
    path('approval/', views.activity_approval, name='activity_approval'),
    path('reports/', views.activity_reports, name='activity_reports'),

    path('api/create/', ActivityCreateAPI.as_view()),
    path('api/list/', ActivityListAPI.as_view()),
    path('api/update/<int:pk>/', ActivityUpdateAPI.as_view()),
    path('api/delete/<int:pk>/', ActivityDeleteAPI.as_view()),

    path('api/approve/<int:pk>/', ActivityApprovalAPI.as_view()),

    path('api/report/daily/', DailyReportAPI.as_view()),
    path('api/report/project/<int:project_id>/', ProjectReportAPI.as_view()),
    path('api/today/', TodayActivityAPI.as_view()),
    path('api/upsert/', ActivityUpsertAPI.as_view()),
    path('api/project-services/<int:project_id>/', ProjectServicesAPI.as_view()),
    path('api/export/', ExportExcelAPI.as_view()),
    path('api/dashboard/', ClientDashboardAPI.as_view()),
    path('api/assignment/delete/<int:id>/', DeleteAssignmentAPI.as_view()),
    path('api/service-modules/<int:service_id>/', ServiceModulesAPI.as_view()),
    path('api/checklist-items/<int:module_id>/', ChecklistItemsAPI.as_view()),
    path('api/task-fields/<int:checklist_id>/', TaskFieldsAPI.as_view(), name='task_fields'),
    path('api/save-activity/',SaveActivityAPI.as_view()),
    

    path('forget_password/', ForgotPasswordAPI.as_view()),
    path('reset_password/', ResetPasswordAPI.as_view()),
    path('api/assigned_work/', AssignedWorkAPI.as_view(), name='assigned_work'),
    path('api/assign-service/', AssignServiceAPI.as_view(), name='assign_service'),
    path(
    "api/detail/<int:pk>/",
    ActivityDetailAPI.as_view()
),
]
