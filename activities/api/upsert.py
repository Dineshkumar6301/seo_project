from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils.dateparse import parse_date
from datetime import date as dt_date

from activities.models import Activity


class ActivityUpsertAPI(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data
        if not data.get("project"):
            return Response(
                {"error": "Project required"},
                status=400
            )

        if not data.get("category"):
            return Response(
                {"error": "Category required"},
                status=400
            )

        if not data.get("service"):
            return Response(
                {"error": "Service required"},
                status=400
            )

        if not data.get("task"):
            return Response(
                {"error": "Task required"},
                status=400
            )

        if not data.get("data"):
            return Response(
                {"error": "Form data required"},
                status=400
            )

        raw_date = data.get("date")

        if not raw_date:
            return Response(
                {"error": "Date required"},
                status=400
            )
        if isinstance(raw_date, str):

            parsed_date = parse_date(raw_date)

            if not parsed_date:

                return Response(
                    {"error": "Invalid date format YYYY-MM-DD"},
                    status=400
                )

            final_date = parsed_date

        elif isinstance(raw_date, dt_date):

            final_date = raw_date

        else:

            return Response(
                {"error": "Invalid date"},
                status=400
            )

        id_value = data.get("id")

        if id_value and str(id_value).isdigit():

            obj = Activity.objects.filter(
                id=int(id_value),
                user=request.user
            ).first()

            if not obj:

                return Response(
                    {"error": "Invalid ID"},
                    status=404
                )

        else:

            obj = Activity()

        obj.user = request.user

        obj.project_id = data.get("project")

        obj.category = data.get("category")

        obj.service_name = data.get("service")

        obj.task_type = data.get("task")

        obj.date = final_date

        obj.dynamic_data = data.get("data")

        obj.status = "pending"

        obj.save()
        activities = Activity.objects.filter(
            user=request.user,
            project_id=data.get("project")
        ).order_by('-id')

        response_data = []

        for a in activities:

            response_data.append({

                "id": a.id,

                "date": str(a.date),

                "project_name": (
                    a.project.name
                    if a.project else ""
                ),

                "category": a.category or "",

                "service": a.service_name or "",

                "task": a.task_type or "",

                "status": a.status or "",

                "submitted_by": (
                    f"{a.user.first_name} {a.user.last_name}".strip()
                    if a.user else ""
                ),

                "data": a.dynamic_data or {}

            })

        # =====================================
        # RESPONSE
        # =====================================
        return Response({

            "id": obj.id,

            "message": "Saved successfully",

            "saved_data": response_data

        })