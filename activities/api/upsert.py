from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from activities.models import Activity


class ActivityUpsertAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data

        # =========================
        # VALIDATION
        # =========================
        if not data.get("project"):
            return Response({"error": "Project required"}, status=400)

        if not data.get("service"):
            return Response({"error": "Service required"}, status=400)

        if not data.get("date"):
            return Response({"error": "Date required"}, status=400)

        # =========================
        # SAFE ID HANDLING (SECURE)
        # =========================
        id_value = data.get("id")
        obj = None

        if id_value and str(id_value).isdigit():
            obj = Activity.objects.filter(
                id=int(id_value),
                user=request.user   # 🔥 SECURITY FIX
            ).first()

            if not obj:
                return Response({"error": "Invalid ID"}, status=404)
        else:
            obj = Activity()

        # =========================
        # ASSIGN DATA (MATCH MODEL)
        # =========================
        obj.user = request.user
        obj.project_id = data.get("project")
        obj.service_id = data.get("service")
        obj.date = data.get("date")

        obj.task_title = data.get("task_title", "")
        obj.keyword = data.get("keyword", "")  # ✅ FIXED
        obj.completed_work = data.get("completed_work", "")
        obj.remarks = data.get("remarks", "")

        # =========================
        # MULTIPLE PROOF LINKS
        # =========================
        proof_links = data.get("proof_links", [])

        if isinstance(proof_links, list):
            obj.proof_link = "\n".join([p.strip() for p in proof_links if p.strip()])
        else:
            obj.proof_link = proof_links or ""

        # =========================
        # BUSINESS RULE
        # =========================
        obj.status = "pending"

        obj.save()

        # =========================
        # RESPONSE
        # =========================
        return Response({
            "id": obj.id,
            "user": request.user.username,
            "message": "Saved successfully"
        })