from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from activities.models import Activity

class ActivityDetailAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        try:

            activity = Activity.objects.get(
                id=pk,
                user=request.user
            )

            return Response({

                "success": True,

                "id": activity.id,

                "project_id": (
                    activity.project.id
                    if activity.project
                    else None
                ),

                "service_id": activity.service_id_ref,

                "module_id": activity.module_id_ref,

                "checklist_id": activity.checklist_id_ref,

                "category": activity.category,

                "service_name": activity.service_name,

                "task_type": activity.task_type,

                "dynamic_data": (
                    activity.dynamic_data
                    or {}
                )
            })

        except Activity.DoesNotExist:

            return Response({

                "success": False,

                "error": "Activity not found"

            }, status=404)

