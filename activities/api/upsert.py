from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from activities.models import Activity


class ActivityUpsertAPI(APIView):

    permission_classes = [IsAuthenticated]   # 🔥 FIX 1

    def post(self, request):

        data = request.data

        # 🔥 VALIDATION
        if not data.get("project"):
            return Response({"error": "Project required"}, status=400)

        if not data.get("service"):
            return Response({"error": "Service required"}, status=400)

        if not data.get("date"):
            return Response({"error": "Date required"}, status=400)

        # 🔥 UPDATE OR CREATE
        if data.get("id"):
            obj = Activity.objects.filter(id=data.get("id")).first()

            if not obj:
                return Response({"error": "Invalid ID"}, status=404)
        else:
            obj = Activity()

        # 🔥 SAVE (SAFE USER)
        obj.user = request.user if request.user.is_authenticated else None

        obj.project_id = data.get("project")
        obj.service_id = data.get("service")
        obj.date = data.get("date")
        obj.task_title = data.get("task_title", "")
        obj.planned_work = data.get("planned_work", "")
        obj.completed_work = data.get("completed_work", "")
        obj.proof_link = data.get("proof_link", "")
        obj.remarks = data.get("remarks", "")

        # 🔥 RESET STATUS ON EDIT
        obj.status = "pending"

        obj.save()

        return Response({
            "id": obj.id,
            "user": request.user.username,   # 🔥 RETURN USER
            "message": "Saved"
        })