from frontend.models import ProjectServiceAssignment
from rest_framework.views import APIView
from rest_framework.response import Response
from activities.models import Activity

class TodayActivityAPI(APIView):
    def get(self, request):

        date = request.GET.get("date")

        assigned_services = ProjectServiceAssignment.objects.filter(
            user=request.user
        ).values_list('service_id', flat=True)

        activities = Activity.objects.filter(
            user=request.user,
            date=date,
            service_id__in=assigned_services   # 🔥 LOCK
        ).select_related("project", "service")

        data = []
        for a in activities:
            data.append({
                "project": a.project_id,
                "project_name": a.project.name,
                "service_name": a.service.name,
                "task_title": a.task_title
            })

        return Response(data)