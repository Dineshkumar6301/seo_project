from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response

from frontend.models import ProjectServiceAssignment

from .models import Project, Service
from .serializers import ProjectSerializer
from clients.models import Client
from accounts.permissions import IsAdminOrManager
from activities.models import Checklist

import json

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

    clients = Client.objects.all() 

    return render(request, 'frontend/projects/list.html', {
        'projects': projects,
        'clients': clients,
    })


@login_required(login_url='home')
def project_create(request):

    if request.user.role not in ['admin', 'manager']:
        return redirect('dashboard')

    clients = Client.objects.all()

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

    projects = Project.objects.select_related('client').all()
    services = Service.objects.all()

    project_id = request.GET.get('project')
    selected_project = None

    if project_id:
        selected_project = get_object_or_404(Project, id=project_id)
    service_team = {}

    if selected_project:

        project_services = selected_project.services.all()

        assignments = ProjectServiceAssignment.objects.filter(
            project_id=selected_project.id
        ).select_related('user', 'service')

        for s in project_services:
            service_team[s.id] = {
                "name": s.name,
                "users": []
            }

        for a in assignments:
            sid = a.service_id

            if sid in service_team:
                service_team[sid]["users"].append(
                    a.user.email or a.user.first_name or "User"
                )
    if request.method == "POST":

        project_id = request.POST.get('project_id')
        selected_services = request.POST.getlist('services')

        project = get_object_or_404(Project, id=project_id)

        try:
            with transaction.atomic():
                project.services.set(selected_services)
                Checklist.objects.filter(project=project).delete()
                services_qs = Service.objects.filter(id__in=selected_services)

                checklist_items = [
                    Checklist(
                        project=project,
                        service=service,
                        item=f"{service.name} - Task",
                        status='Approved'
                    )
                    for service in services_qs
                ]

                Checklist.objects.bulk_create(checklist_items)

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")

        return redirect(f'/projects/project-dashboard/?project={project_id}')

    return render(request, 'frontend/projects/dashboard.html', {
        'projects': projects,
        'services': services,
        'selected_project': selected_project,
        'service_team': service_team
    })


@login_required(login_url='home')
@require_POST
def add_service(request):

    try:
        data = json.loads(request.body)
        name = data.get("name", "").strip()

        if not name:
            return JsonResponse({"error": "Service name required"}, status=400)

        service, created = Service.objects.get_or_create(name=name)

        return JsonResponse({
            "success": True,
            "id": service.id,
            "name": service.name,
            "created": created
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from activities.models import Activity

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
    

