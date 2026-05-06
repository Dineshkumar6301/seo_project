from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils.dateparse import parse_date
from datetime import timedelta

from activities.models import Activity


class ActivityListAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        date_str = request.GET.get("date")

        type_filter = request.GET.get("type")

        start_date = request.GET.get("start_date")

        end_date = request.GET.get("end_date")

        project = request.GET.get("project")

        # =====================================
        # BASE QUERY
        # =====================================
        qs = Activity.objects.filter(
            user=request.user
        )

        # =====================================
        # PROJECT FILTER
        # =====================================
        if project:

            qs = qs.filter(
                project_id=project
            )

        # =====================================
        # DATE FILTERS
        # =====================================
        base_date = (
            parse_date(date_str)
            if date_str else None
        )

        # CUSTOM RANGE
        if start_date or end_date:

            if start_date:

                qs = qs.filter(
                    date__gte=start_date
                )

            if end_date:

                qs = qs.filter(
                    date__lte=end_date
                )

        else:

            # TODAY
            if type_filter == "today" and base_date:

                qs = qs.filter(
                    date=base_date
                )

            # LAST WEEK
            elif type_filter == "week" and base_date:

                qs = qs.filter(
                    date__gte=base_date - timedelta(days=7)
                )

            # LAST MONTH
            elif type_filter == "month" and base_date:

                qs = qs.filter(
                    date__month=base_date.month
                )

            # SINGLE DATE
            elif base_date:

                qs = qs.filter(
                    date=base_date
                )

        # =====================================
        # ORDERING
        # =====================================
        qs = qs.order_by("-id")

        # =====================================
        # RESPONSE
        # =====================================
        response_data = []

        for a in qs:

            response_data.append({

                "id": a.id,

                "date": str(a.date),

                "project": (
                    a.project.name
                    if a.project else ""
                ),

                "project_name": (
                    a.project.name
                    if a.project else ""
                ),

                "category": (
                    a.category or ""
                ),

                "service": (
                    a.service_name or ""
                ),

                "task": (
                    a.task_type or ""
                ),

                "status": (
                    a.status or ""
                ),

                "data": (
                    a.dynamic_data or {}
                )
            })

        return Response(response_data)