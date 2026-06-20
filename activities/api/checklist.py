from rest_framework.views import APIView
from rest_framework.response import Response

from projects.models import ChecklistTemplate



class ChecklistItemsAPI(APIView):

    def get(self, request, module_id):

        checklists = ChecklistTemplate.objects.filter(
            module_id=module_id,
            is_active=True
        ).order_by("order")

        data = []

        for item in checklists:

            data.append({
                "id": item.id,
                "item": item.item
            })

        return Response(data)

