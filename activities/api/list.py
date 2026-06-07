from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.utils.dateparse import parse_date
from datetime import timedelta, date

from activities.models import Activity

class ActivityListAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        date_str = request.GET.get("date")
        filter_type = request.GET.get("filter")
        start_date = request.GET.get("start")
        end_date = request.GET.get("end")
        project = request.GET.get("project")

        qs = Activity.objects.select_related(
            "project"
        ).filter(
            user=request.user
        )

        if project and project != "all":
            qs = qs.filter(
                project_id=project
            )

        if date_str:
            base_date = parse_date(date_str)
        else:
            base_date = date.today()

        if start_date:
            qs = qs.filter(
                date__gte=start_date
            )

        if end_date:
            qs = qs.filter(
                date__lte=end_date
            )

        elif filter_type == "today":

            qs = qs.filter(
                date=base_date
            )

        elif filter_type == "week":

            start_week = (
                base_date -
                timedelta(days=base_date.weekday())
            )

            end_week = (
                start_week +
                timedelta(days=6)
            )

            qs = qs.filter(
                date__range=[
                    start_week,
                    end_week
                ]
            )

        elif filter_type == "month":

            qs = qs.filter(
                date__month=base_date.month,
                date__year=base_date.year
            )

        elif filter_type == "year":

            qs = qs.filter(
                date__year=base_date.year
            )

        else:

            qs = qs.filter(
                date=base_date
            )

        # IMPORTANT OPTIMIZATION
        qs = qs.order_by(
            "-date",
            "-id"
        )[:500]

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