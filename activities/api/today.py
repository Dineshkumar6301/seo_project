from frontend.models import ProjectServiceAssignment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from activities.models import Activity


class TodayActivityAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        date = request.GET.get("date")

        if not date:
            return Response({"error": "Date is required"}, status=400)

        # 🔥 GET ASSIGNMENTS
        assignments = ProjectServiceAssignment.objects.filter(
            user=request.user
        )

        assigned_services = assignments.values_list('service_id', flat=True)
        assigned_projects = assignments.values_list('project_id', flat=True)

        # 🔥 STRICT FILTER
        activities = Activity.objects.filter(
            user=request.user,
            date=date,
            service_id__in=assigned_services,
            project_id__in=assigned_projects
        ).select_related("project", "service")

        data = [
            {
                "id": a.id,
                "project": a.project_id,
                "project_name": a.project.name,
                "service": a.service_id,
                "service_name": a.service.name,
                "task_title": a.task_title,
                "planned_work": a.planned_work,
                "completed_work": a.completed_work,
                "proof_links": a.proof_link.split("\n") if a.proof_link else [],
                "remarks": a.remarks,
                "status": a.status,
            }
            for a in activities
        ]

        return Response(data)