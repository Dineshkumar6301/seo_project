from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from frontend.models import ProjectServiceAssignment
from .models import Project, Service, ServiceCategory, ProjectService
from .serializers import ProjectSerializer
from clients.models import Client
from accounts.permissions import IsAdminOrManager
from .models import (
    Project,
    Service,
    ServiceCategory,
    ProjectService,
    ProjectChecklist,
    ChecklistTemplate,
)
from collections import defaultdict
from accounts.models import User
import json
from django.views import View
from frontend.models import ProjectServiceAssignment
from django.contrib.auth.mixins import LoginRequiredMixin
from clients.models import ClientOnboarding


class ProjectCreateAPI(APIView):
    permission_classes = [IsAdminOrManager]

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({
                "message": "Project created successfully",
                "data": serializer.data
            }, status=201)

        return Response(serializer.errors, status=400)

@login_required(login_url='home')
def project_list(request):

    if request.user.role == 'client':
        client = Client.objects.filter(user=request.user).first()
        projects = Project.objects.filter(client=client) if client else []
    else:
        projects = Project.objects.select_related('client').all()

    clients = Client.objects.all().order_by('name') 

    return render(request, 'frontend/projects/list.html', {
        'projects': projects,
        'clients': clients,
    })


@login_required(login_url='home')
def project_create(request):

    if request.user.role not in ['admin', 'manager']:
        return redirect('dashboard')

    clients = Client.objects.all().order_by('name')

    if request.method == "POST":
        name = request.POST.get('name')
        client_id = request.POST.get('client')
        start_date = request.POST.get('start_date')

        if not name or not client_id:
            return HttpResponseBadRequest("Missing required fields")

        Project.objects.create(
            name=name,
            client_id=client_id,
            start_date=start_date,
            owner=request.user
        )

        return redirect('project_list')

    return render(request, 'frontend/projects/create.html', {
        'clients': clients
    })

@login_required(login_url='home')
def project_dashboard(request):

    users = User.objects.filter(
        is_active=True
    ).exclude(role='client')

    projects = Project.objects.select_related(
        'client'
    ).order_by('name')

    selected_project = None
    project_services = []

    project_id = request.GET.get('project')

    if project_id:

        selected_project = get_object_or_404(
            Project,
            id=project_id
        )

        project_services = (
            ProjectService.objects
            .filter(project=selected_project)
            .select_related(
                'service',
                'service__category'
            )
        )

    services_grouped = defaultdict(list)

    for ps in project_services:

        category_name = (
            ps.service.category.name
            if ps.service.category
            else "Other"
        )

        services_grouped[category_name].append(
            ps.service
        )

    service_team = {}

    if selected_project:

        assignments = (
            ProjectServiceAssignment.objects
            .filter(project=selected_project)
            .select_related(
                'user',
                'service'
            )
        )

        for ps in project_services:

            service_team[ps.service.id] = {
                "name": ps.service.name,
                "users": []
            }

        for a in assignments:

            if a.service_id in service_team:

                service_team[a.service_id]["users"].append({
                    "id": a.user.id,
                    "name": (
                        a.user.first_name
                        or a.user.email
                        or "User"
                    )
                })

    # SAVE SERVICES
    if request.method == "POST":

        project_id = request.POST.get(
            "project_id"
        )

        selected_services = request.POST.getlist(
            "services"
        )

        project = get_object_or_404(
            Project,
            id=project_id
        )

        try:

            with transaction.atomic():

                # Remove unselected services
                ProjectService.objects.filter(
                    project=project
                ).exclude(
                    service_id__in=selected_services
                ).delete()

                existing_service_ids = set(
                    ProjectService.objects.filter(
                        project=project
                    ).values_list(
                        "service_id",
                        flat=True
                    )
                )

                # Add newly selected services
                for sid in selected_services:

                    if int(sid) not in existing_service_ids:

                        ProjectService.objects.create(
                            project=project,
                            service_id=sid
                        )

                # Rebuild project checklist
                ProjectChecklist.objects.filter(
                    project=project
                ).delete()

                services = Service.objects.filter(
                    id__in=selected_services
                )

                project_checklists = []

                for service in services:

                    templates = ChecklistTemplate.objects.filter(
                        module__service=service,
                        is_active=True
                    ).select_related(
                        "module"
                    )

                    for template in templates:

                        project_checklists.append(

                            ProjectChecklist(
                                project=project,
                                template=template,
                                status="Approved"
                            )

                        )

                ProjectChecklist.objects.bulk_create(
                    project_checklists,
                    ignore_conflicts=True
                )

        except Exception as e:

            return HttpResponseBadRequest(
                f"Error: {str(e)}"
            )

        return redirect(
            f"/projects/project-dashboard/?project={project_id}"
        )

    all_services = (
        Service.objects
        .select_related("category")
        .order_by(
            "category__name",
            "name"
        )
    )

    project_checklists = []

    if selected_project:

        project_checklists = (
            ProjectChecklist.objects
            .filter(
                project=selected_project
            )
            .select_related(
                "template",
                "template__module",
                "template__module__service"
            )
            .order_by(
                "template__module__service__name",
                "template__module__order",
                "template__order"
            )
        )
    onboarding = None

    progress = 0

    if selected_project:

        onboarding = ClientOnboarding.objects.filter(
            client=selected_project.client
        ).first()

        if onboarding:

            completed = sum([

                onboarding.hosting_access,
                onboarding.domain_access,
                onboarding.ga_access,
                onboarding.gsc_access,
               
                onboarding.google_ads_access,
                onboarding.meta_access,
                onboarding.youtube_access,
                onboarding.social_media_access,
                onboarding.team_assigned,
                onboarding.kpi_defined,
                onboarding.deliverables_defined,
                onboarding.reporting_setup,
            ])

            progress = int(
                (completed / 12) * 100
            )

    selected_service_ids = []

    if selected_project:
        selected_service_ids = list(
            selected_project.project_services.values_list(
                "service_id",
                flat=True
            )
        )    
    return render(
        request,
        "frontend/projects/dashboard.html",
        {
            "projects": projects,
            "all_services": all_services,
            "services_grouped": dict(
                services_grouped
            ),
            "selected_project": selected_project,
            "service_team": service_team,
            "users": users,
            "project_checklists": project_checklists,
            "onboarding": onboarding,
            "onboarding_progress": progress,
            "selected_service_ids": selected_service_ids,
        }
    )






@login_required(login_url='home')
@require_POST
def add_service(request):

    data = json.loads(request.body)

    name = data.get("name")
    category_name = data.get("category")

    if not name or not category_name:

        return JsonResponse({
            "error": "Missing data"
        }, status=400)

    category, _ = ServiceCategory.objects.get_or_create(
        name=category_name
    )

    service, created = Service.objects.get_or_create(
        name=name,
        defaults={
            "category": category
        }
    )

    if service.category != category:

        service.category = category
        service.save()

    return JsonResponse({

        "success": True,

        "id": service.id,

        "name": service.name,

        "category": (
            service.category.name
            if service.category
            else ""
        )
    })


@login_required
def project_update(request, pk):

    project = Project.objects.get(id=pk)

    if request.method == "POST":

        data = json.loads(request.body)

        project.name = data.get('name')
        project.client_id = data.get('client')
        project.start_date = data.get('start_date')

        project.save()

        return JsonResponse({"success": True})
    

class RemoveUserFromService(LoginRequiredMixin, View):

    def post(self, request):
        try:
            data = json.loads(request.body)

            service_id = data.get('service_id')
            user_id = data.get('user_id')

            print("DEBUG:", service_id, user_id)  # 🔥 debug log

            if not service_id or not user_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Missing service_id or user_id'
                }, status=400)

            deleted_count, _ = ProjectServiceAssignment.objects.filter(
                service_id=service_id,
                user_id=user_id
            ).delete()

            if deleted_count == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Assignment not found'
                }, status=404)

            return JsonResponse({
                'status': 'success',
                'message': 'User removed successfully'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
        


from django.shortcuts import render
from django.http import JsonResponse
from projects.models import Project
from activities.models import Activity

import requests
from urllib.parse import urlparse


def rank_page(request):

    projects = Project.objects.all().order_by("name")

    return render(
        request,
        "frontend/rank.html",
        {
            "projects": projects
        }
    )


def get_project_rank_data(request):

    project_id = request.GET.get("project_id")

    if not project_id:

        return JsonResponse({
            "success": False
        })

    project = Project.objects.select_related(
        "client"
    ).get(id=project_id)

    activities = Activity.objects.filter(
        project_id=project_id,
        status="approved"
    )

    keywords = set()
    website = project.client.website

    for activity in activities:

        data = activity.dynamic_data or {}

        keyword = data.get("Keyword")

        if keyword:
            keywords.add(keyword)

    return JsonResponse({
        "success": True,
        "website": website,
        "keywords": sorted(list(keywords))
    })


def check_keyword_rank(request):

    keyword = request.GET.get("keyword")
    website = request.GET.get("website")

    if not keyword or not website:

        return JsonResponse({
            "success": False,
            "message": "Keyword and website are required"
        })

    try:

        response = requests.post(
            "https://api.apyhub.com/extract/serp/rank?location=in&language=en",
            headers={
                "apy-token": "APY0bkk9F6VgGb2oBgEQGKQTLnG0KL8MRwHb4NMzMoBhSonvORBfaPdRxtIcx4MRM",
                "Content-Type": "application/json"
            },
            json={
                "keyword": keyword
            },
            timeout=60
        )

        api_data = response.json()

        domain = (
            urlparse(website)
            .netloc
            .replace("www.", "")
            .lower()
        )

        rank_found = None
        matched_url = None

        for item in api_data.get("data", []):

            result_url = item.get("url", "")

            if not result_url:
                continue

            result_domain = (
                urlparse(result_url)
                .netloc
                .replace("www.", "")
                .lower()
            )

            if domain == result_domain:

                rank_found = item.get("rank")
                matched_url = result_url

                break

        if rank_found is None:

            return JsonResponse({
                "success": True,
                "keyword": keyword,
                "website": website,
                "position": "Not Found (Top Results)",
                "url": "-"
            })

        return JsonResponse({
            "success": True,
            "keyword": keyword,
            "website": website,
            "position": rank_found,
            "url": matched_url
        })
    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


from django.http import JsonResponse
from projects.models import KeywordRank


def project_rank_results(request):

    project_id = request.GET.get("project_id")

    data = KeywordRank.objects.filter(
        project_id=project_id
    ).order_by("-checked_at")

    results = []

    for item in data:

        results.append({
            "keyword": item.keyword,
            "rank": item.rank if item.rank else "Not Ranking",
            "url": item.ranking_url or "-",
            "checked_at": item.checked_at.strftime("%d-%m-%Y %H:%M")
        })

    return JsonResponse({
        "success": True,
        "results": results
    })