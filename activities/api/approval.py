from rest_framework.views import APIView
from rest_framework.response import Response
from activities.models import Activity


class ActivityApprovalAPI(APIView):

    def post(self, request, pk):

        activity = Activity.objects.filter(id=pk).first()

        if not activity:
            return Response({"error": "Not found"}, status=404)

        status = request.data.get("status")

        if status not in ["approved", "rejected"]:
            return Response({"error": "Invalid status"}, status=400)

        activity.status = status
        activity.save()

        return Response({"success": True})