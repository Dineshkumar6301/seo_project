from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from frontend.models import ProjectServiceAssignment


class AssignedWorkAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        assignments = ProjectServiceAssignment.objects.filter(
            user=request.user
        ).select_related("project", "service")

        data = {}

        for a in assignments:

            project_id = a.project.id

            if project_id not in data:
                data[project_id] = {
                    "project_name": a.project.name,
                    "services": []
                }

            data[project_id]["services"].append({
                "id": a.service.id,
                "name": a.service.name
                
            })

        print("FINAL DATA:", data)  # DEBUG

        return Response(data)