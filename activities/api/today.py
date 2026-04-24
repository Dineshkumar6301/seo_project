from frontend.models import ProjectServiceAssignment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from activities.models import Activity


class TodayActivityAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # =========================
        # 🔥 GET DATE
        # =========================
        date = request.GET.get("date")

        if not date:
            return Response({"error": "Date is required"}, status=400)

        # =========================
        # 🔥 GET ASSIGNED SERVICES
        # =========================
        assigned_services = ProjectServiceAssignment.objects.filter(
            user=request.user
        ).values_list('service_id', flat=True)

        # =========================
        # 🔥 FILTER ACTIVITIES
        # =========================
        activities = Activity.objects.filter(
            user=request.user,
            date=date,
            service_id__in=assigned_services
        ).select_related("project", "service")

        # =========================
        # 🔥 RESPONSE DATA (IMPORTANT FIX)
        # =========================
        data = [
            {
                "id": a.id,  # ✅ REQUIRED for update
                "project": a.project_id,  # ✅ REQUIRED for dropdown
                "project_name": a.project.name,
                "service": a.service_id,  # ✅ REQUIRED for dropdown
                "service_name": a.service.name,
                "task_title": a.task_title,
                "planned_work": a.planned_work,
                "completed_work": a.completed_work,
                "proof_link": a.proof_link,
                "remarks": a.remarks,
                "status": a.status,
            }
            for a in activities
        ]

        return Response(data)