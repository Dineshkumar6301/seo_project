from rest_framework.views import APIView
from rest_framework.response import Response
from activities.models import Activity


class ActivityUpdateAPI(APIView):

    def post(self, request, pk):

        obj = Activity.objects.filter(id=pk).first()

        if not obj:
            return Response({"error": "Not found"}, status=404)

        obj.task_title = request.data.get("task_title", obj.task_title)
        obj.planned_work = request.data.get("planned_work", obj.planned_work)
        obj.completed_work = request.data.get("completed_work", obj.completed_work)
        obj.proof_link = request.data.get("proof_link", obj.proof_link)
        obj.remarks = request.data.get("remarks", obj.remarks)

        obj.save()

        return Response({"success": True})