from rest_framework.views import APIView
from rest_framework.response import Response
from frontend.models import ProjectServiceAssignment


class ProjectServiceAPI(APIView):

    def get(self, request, project_id):

        user = request.user

        
        assignments = ProjectServiceAssignment.objects.filter(
            project_id=project_id,
            user=user
        ).select_related('service')

        return Response([
            {
                "id": a.service.id,
                "name": a.service.name
            }
            for a in assignments
        ])