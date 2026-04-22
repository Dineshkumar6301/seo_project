from django.urls import path

from . import views
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
from django.urls import path
from activities.api.today import TodayActivityAPI
from activities.api.upsert import ActivityUpsertAPI
from activities.api.export import ExportExcelAPI
from activities.api.project_services import ProjectServiceAPI

urlpatterns = [

    # 🔥 UI ROUTES (IMPORTANT FIX)
    path('daily/', views.activity_daily, name='activity_daily'),
    path('approval/', views.activity_approval, name='activity_approval'),
    path('reports/', views.activity_reports, name='activity_reports'),

    # 🔹 API ROUTES
    path('api/create/', ActivityCreateAPI.as_view()),
    path('api/list/', ActivityListAPI.as_view()),
    path('api/update/<int:pk>/', ActivityUpdateAPI.as_view()),
    path('api/delete/<int:pk>/', ActivityDeleteAPI.as_view()),

    path('api/approve/<int:pk>/', ActivityApprovalAPI.as_view()),

    path('api/report/daily/', DailyReportAPI.as_view()),
    path('api/report/project/<int:project_id>/', ProjectReportAPI.as_view()),
    path('api/today/', TodayActivityAPI.as_view()),
    path('api/upsert/', ActivityUpsertAPI.as_view()),
    path('api/project-services/<int:project_id>/', ProjectServiceAPI.as_view()),
    path('api/export/', ExportExcelAPI.as_view()),
    # activities/urls.py
    path('api/dashboard/', ClientDashboardAPI.as_view()),
    path('api/assignment/delete/<int:id>/', DeleteAssignmentAPI.as_view()),
    path('export-report/', views.export_report, name='export_report'),

]