from rest_framework.views import APIView
from rest_framework.response import Response
from projects.models import ServiceTask



from rest_framework.views import APIView
from rest_framework.response import Response

from projects.models import (
    ProjectService,
    ServiceTask
)


class ProjectServiceAPI(APIView):

    def get(self, request, project_id):

        data = {}

        project_services = ProjectService.objects.filter(
            project_id=project_id
        ).select_related(
            'service',
            'service__category'
        )

        for ps in project_services:

            service = ps.service

            category_name = (
                service.category.name
                if service.category
                else "Other"
            )

            if category_name not in data:
                data[category_name] = {}

            if service.name not in data[category_name]:
                data[category_name][service.name] = {}

            tasks = ServiceTask.objects.filter(
                service=service,
                is_active=True
            ).prefetch_related('fields')

            for task in tasks:

                data[category_name][service.name][task.name] = [

                    {
                        "name": f.name,
                        "label": f.label,
                        "type": f.field_type,
                        "required": f.required,
                        "options": f.options or []
                    }

                    for f in task.fields.all().order_by('order')
                ]

        return Response(data)

