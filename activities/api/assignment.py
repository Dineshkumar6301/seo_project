from rest_framework.views import APIView
from rest_framework.response import Response
from frontend.models import ProjectServiceAssignment


class DeleteAssignmentAPI(APIView):

    def post(self, request, id):
        obj = ProjectServiceAssignment.objects.filter(id=id).first()

        if not obj:
            return Response({"error": "Not found"}, status=404)

        obj.delete()
        return Response({"success": True})


