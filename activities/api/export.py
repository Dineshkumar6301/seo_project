# activities/api/export.py
from rest_framework.views import APIView
from django.http import HttpResponse
from openpyxl import Workbook
from ..models import Activity

class ExportExcelAPI(APIView):
    def get(self, request):
        date = request.GET.get('date')
        qs = Activity.objects.filter(user=request.user, date=date)

        wb = Workbook()
        ws = wb.active
        ws.title = "Daily Sheet"

        headers = ["Employee", "Project", "Task", "Type", "Planned", "Completed", "Proof", "Remarks"]
        ws.append(headers)

        for a in qs:
            ws.append([
                a.user.username,
                a.project.name,
                a.task_title,
                a.task_type,
                a.planned_work,
                a.completed_work,
                a.proof_link,
                a.remarks
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = f'attachment; filename=activity_{date}.xlsx'
        wb.save(response)
        return response