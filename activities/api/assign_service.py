from rest_framework.views import APIView
from rest_framework.response import Response
from frontend.models import ProjectServiceAssignment


class AssignServiceAPI(APIView):

    def post(self, request):

        user_id = request.data.get("user_id")
        service_id = request.data.get("service_id")
        project_id = request.data.get("project_id")

        if not user_id or not service_id or not project_id:
            return Response({"error": "Missing data"}, status=400)

        exists = ProjectServiceAssignment.objects.filter(
            user_id=user_id,
            service_id=service_id,
            project_id=project_id
        ).exists()

        if exists:
            return Response({"error": "Already assigned"}, status=400)

        ProjectServiceAssignment.objects.create(
            user_id=user_id,
            service_id=service_id,
            project_id=project_id
        )

        return Response({"success": True})