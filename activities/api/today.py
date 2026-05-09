from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from activities.models import Activity


class TodayActivityAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        date_str = request.GET.get("date")

        if not date_str:

            return Response({
                "error": "Date is required"
            }, status=400)

        try:

            date = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            return Response({
                "error": "Invalid date format"
            }, status=400)

        # =====================================
        # FETCH ACTIVITIES
        # =====================================

        activities = Activity.objects.filter(
            user=request.user,
            date=date
        ).select_related("project")

        # =====================================
        # RESPONSE
        # =====================================

        response_data = []

        for activity in activities:

            dynamic_data = (
                activity.dynamic_data or {}
            )

            response_data.append({

                "id": activity.id,

                "project": (
                    activity.project.id
                    if activity.project else None
                ),

                "project_name": (
                    activity.project.name
                    if activity.project else ""
                ),

                "category": (
                    activity.category or ""
                ),

                "service_name": (
                    activity.service_name or ""
                ),

                "task_type": (
                    activity.task_type or ""
                ),

                "dynamic_data": dynamic_data,

                # FRONTEND TABLE SUPPORT
                "SUBMITTED_URL": (
                    dynamic_data.get(
                        "submitted_url",
                        ""
                    )
                ),

                "status": (
                    activity.status or ""
                ),

                "date": str(activity.date)
            })

        return Response(response_data)