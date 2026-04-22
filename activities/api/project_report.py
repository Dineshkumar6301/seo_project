
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from activities.models import Activity
class ProjectReportAPI(APIView):

    def get(self, request, project_id):

        activities = Activity.objects.filter(
            project_id=project_id,
            status='approved'
        )

        return Response({
            "project": project_id,
            "total_tasks": activities.count()
        })