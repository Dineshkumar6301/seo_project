from rest_framework.views import APIView
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from django.db.models import Q
from django.utils.timezone import now
from datetime import timedelta
from activities.models import Activity

class ExportExcelAPI(APIView):

    def get(self, request):

        qs = Activity.objects.all()

    
        if hasattr(request.user, "client"):
            qs = qs.filter(project__client=request.user.client)

    
        filter_type = request.GET.get("type")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        search = request.GET.get("search")
        status = request.GET.get("status")
        project = request.GET.get("project")
        service = request.GET.get("service")

        today = now().date()

        
                # ✅ Custom range overrides filter type
        if start_date or end_date:
            if start_date:
                qs = qs.filter(date__gte=start_date)
            if end_date:
                qs = qs.filter(date__lte=end_date)

        else:
            if filter_type == "today":
                qs = qs.filter(date=today)
            elif filter_type == "week":
                qs = qs.filter(date__gte=today - timedelta(days=7))
            elif filter_type == "month":
                qs = qs.filter(date__month=today.month)

        
        if status:
            qs = qs.filter(status=status)

        
        if project:
            qs = qs.filter(project__id=project)

        
        if service:
            qs = qs.filter(service__name__iexact=service.strip())

        if search:
            qs = qs.filter(
                Q(task_title__icontains=search) |
                Q(keyword__icontains=search) |
                Q(project__name__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        wb = Workbook()
        ws = wb.active
        ws.title = "Activity Report"

    
        ws.merge_cells("A1:J1")
        ws["A1"] = "CLIENT ACTIVITY REPORT"
        ws["A1"].font = Font(size=16, bold=True)
        ws["A1"].alignment = Alignment(horizontal="center")

    
        ws.merge_cells("A2:J2")
        ws["A2"] = f"Date: {start_date or 'All'} → {end_date or 'All'} | Search: {search or 'None'}"
        ws["A2"].alignment = Alignment(horizontal="center")

        headers = [
            "S.No","Employee","Project","Service",
            "Task","Keyword","Completed Work",
            "Proof Links","Status","Date"
        ]

        ws.append(headers)

        header_fill = PatternFill(start_color="4F46E5", fill_type="solid")
        header_font = Font(color="FFFFFF", bold=True)

        for cell in ws[3]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")

    
        row_num = 4
        serial = 1


        for a in qs:

            links = [l.strip() for l in str(a.proof_link).splitlines() if l.strip()] or [""]

            start_row = row_num

            for i, link in enumerate(links):

                ws.cell(row=row_num, column=1, value=serial if i == 0 else "")
                ws.cell(row=row_num, column=2, value=f"{a.user.first_name} {a.user.last_name}" if i == 0 else "")
                ws.cell(row=row_num, column=3, value=a.project.name if i == 0 else "")
                ws.cell(row=row_num, column=4, value=a.service.name if i == 0 else "")
                ws.cell(row=row_num, column=5, value=a.task_title if i == 0 else "")
                ws.cell(row=row_num, column=6, value=a.keyword if i == 0 else "")
                ws.cell(row=row_num, column=7, value=a.completed_work if i == 0 else "")
                ws.cell(row=row_num, column=8, value=link)
                ws.cell(row=row_num, column=9, value=a.status if i == 0 else "")
                ws.cell(row=row_num, column=10, value=str(a.date) if i == 0 else "")

                if link:
                    ws.cell(row=row_num, column=8).hyperlink = link

                row_num += 1

            end_row = row_num - 1

            if end_row > start_row:
                for col in [1,2,3,4,5,6,7,9,10]:
                    ws.merge_cells(start_row=start_row, start_column=col, end_row=end_row, end_column=col)

            serial += 1
            

        
        for row in ws.iter_rows(min_row=4):
            cell = row[7] 

            if cell.value:
                link = str(cell.value).strip()

            
                if not link.startswith("http"):
                    link = "https://" + link

                cell.value = link
                cell.hyperlink = link
                cell.font = Font(color="0563C1", underline="single")


                border = Border(
                    left=Side(style="thin"),
                    right=Side(style="thin"),
                    top=Side(style="thin"),
                    bottom=Side(style="thin")
                )

        for row in ws.iter_rows():
            for cell in row:
                cell.border = border
                cell.alignment = Alignment(wrap_text=True, vertical="top")

        widths = [6,20,22,18,30,20,30,45,15,15]
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[chr(64+i)].width = w

        ws.freeze_panes = "A4"
        ws.auto_filter.ref = "A3:J3"

        filename = f"report_{start_date or 'all'}_{end_date or 'all'}.xlsx"

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"

        wb.save(response)
        return response