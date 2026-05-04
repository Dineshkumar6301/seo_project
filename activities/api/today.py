from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from frontend.models import ProjectServiceAssignment
from activities.models import Activity


class TodayActivityAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # ✅ Get date from request
        date_str = request.GET.get("date")
        if not date_str:
            return Response({"error": "Date is required"}, status=400)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=400)

        # ✅ Get only assignments for this user
        assignments = ProjectServiceAssignment.objects.filter(
            user=request.user
        ).select_related("project", "service")

        data = []

        for a in assignments:

            # ✅ Ensure only ONE activity per day
            activity, _ = Activity.objects.get_or_create(
                user=request.user,
                project=a.project,
                service=a.service,
                date=date
            )

            data.append({
                "id": activity.id,
                "project": a.project.id,
                "project_name": a.project.name,
                "service": a.service.id,
                "service_name": a.service.name,
                "task_title": activity.task_title,
                "keyword": activity.keyword,
                "completed_work": activity.completed_work,
                "proof_links": activity.proof_link.split("\n") if activity.proof_link else [],
                "remarks": activity.remarks,
                "status": activity.status,
            })

        return Response(data)