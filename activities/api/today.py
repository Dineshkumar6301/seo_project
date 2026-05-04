from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from activities.models import Activity


class TodayActivityAPI(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):

        date_str = request.GET.get("date")

        if not date_str:
            return Response({"error": "Date is required"}, status=400)

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format"}, status=400)

        # ✅ ONLY FETCH SAVED DATA
        activities = Activity.objects.filter(
            user=request.user,
            date=date
        ).select_related("project", "service")

        data = []

        for activity in activities:
            data.append({
                "id": activity.id,
                "project": activity.project.id,
                "project_name": activity.project.name,
                "service": activity.service.id,
                "service_name": activity.service.name,
                "task_title": activity.task_title,
                "keyword": activity.keyword,
                "completed_work": activity.completed_work,
                "proof_links": activity.proof_link.split("\n") if activity.proof_link else [],
                "remarks": activity.remarks,
                "status": activity.status,
            })

        return Response(data)