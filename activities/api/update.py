from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from activities.models import Activity


class ActivityUpdateAPI(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        try:

            activity = Activity.objects.get(id=pk)

        except Activity.DoesNotExist:

            return Response({
                "error": "Activity not found"
            }, status=404)

        data = request.data
        activity.project_id = data.get("project")

        activity.category = data.get("category")

        activity.service_name = data.get("service_name")

        activity.task_type = data.get("task_type")

        activity.dynamic_data = data.get(
            "dynamic_data",
            {}
        )

        activity.save()

        return Response({
            "success": True,
            "message": "Updated successfully"
        })