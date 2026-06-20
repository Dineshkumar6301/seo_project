from rest_framework.views import APIView
from rest_framework.response import Response

from projects.models import (
    ServiceModule,
    ChecklistTemplate,
    TaskField
)


class ServiceModulesAPI(APIView):

    def get(self, request, service_id):

        modules = ServiceModule.objects.filter(
            service_id=service_id,
            is_active=True
        ).order_by("order")

        data = []

        for module in modules:

            data.append({
                "id": module.id,
                "name": module.name
            })

        return Response(data)



