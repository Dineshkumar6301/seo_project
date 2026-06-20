from rest_framework.views import APIView
from rest_framework.response import Response

from projects.models import TaskField

class TaskFieldsAPI(APIView):

    def get(self, request, checklist_id):

        fields = TaskField.objects.filter(
            checklist_template_id=checklist_id
        ).order_by("order")

        data = []

        for field in fields:

            data.append({
                "id": field.id,
                "label": field.label,
                "name": field.field_name,
                "field_type": field.field_type,
                "required": field.required,
                "options": field.options
            })

        return Response(data)