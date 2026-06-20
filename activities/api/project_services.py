from rest_framework.views import APIView
from rest_framework.response import Response

from projects.models import ProjectService


from rest_framework.views import APIView
from rest_framework.response import Response

from projects.models import ProjectService


class ProjectServicesAPI(APIView):

    def get(self, request, project_id):

        services = (
            ProjectService.objects
            .filter(project_id=project_id)
            .select_related(
                "service",
                "service__category"
            )
        )

        data = []

        for ps in services:

            data.append({

                "id": ps.service.id,

                "name": ps.service.name,

                "category_name": (
                    ps.service.category.name
                    if ps.service.category
                    else "Others"
                )
            })

        return Response(data)