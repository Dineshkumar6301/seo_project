from rest_framework.views import APIView
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill
from ..models import Activity


class ExportExcelAPI(APIView):

    def get(self, request):

        date = request.GET.get('date')
        qs = Activity.objects.filter(user=request.user, date=date).select_related(
            'project', 'service'
        )

        wb = Workbook()
        ws = wb.active
        ws.title = "Daily Sheet"

        # =========================
        # HEADER
        # =========================
        headers = [
            "S.No", "Employee", "Project", "Service",
            "Task", "Keyword", "Completed",
            "Proof Links", "Remarks"
        ]
        ws.append(headers)

        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="4F46E5", fill_type="solid")
        center = Alignment(horizontal="center", vertical="center")
        wrap = Alignment(wrap_text=True, vertical="top")

        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = center

        # =========================
        # DATA
        # =========================
        row_num = 2
        serial = 1

        for a in qs:

            # 🔥 SPLIT LINKS
            if a.proof_link:
                links = [l.strip() for l in str(a.proof_link).splitlines() if l.strip()]
            else:
                links = [""]

            start_row = row_num

            for i, link in enumerate(links):

                ws.cell(row=row_num, column=1, value=serial if i == 0 else "")
                ws.cell(
    row=row_num,
    column=2,
    value=f"{a.user.first_name} {a.user.last_name}" if i == 0 else ""
)
                ws.cell(row=row_num, column=3, value=a.project.name if i == 0 else "")
                ws.cell(row=row_num, column=4, value=a.service.name if a.service and i == 0 else "")
                ws.cell(row=row_num, column=5, value=a.task_title if i == 0 else "")
                ws.cell(row=row_num, column=6, value=a.keyword if i == 0 else "")
                ws.cell(row=row_num, column=7, value=a.completed_work if i == 0 else "")
                ws.cell(row=row_num, column=8, value=link)
                ws.cell(row=row_num, column=9, value=a.remarks if i == 0 else "")

                # 🔗 CLICKABLE LINK
                if link:
                    cell = ws.cell(row=row_num, column=8)
                    cell.hyperlink = link
                    cell.style = "Hyperlink"

                row_num += 1

            end_row = row_num - 1

            # =========================
            # MERGE CELLS (skip Proof column 8)
            # =========================
            if end_row > start_row:
                for col in [1, 2, 3, 4, 5, 6, 7, 9]:
                    ws.merge_cells(
                        start_row=start_row,
                        start_column=col,
                        end_row=end_row,
                        end_column=col
                    )

            serial += 1

        # =========================
        # STYLING
        # =========================
        thin = Side(style="thin")
        border = Border(left=thin, right=thin, top=thin, bottom=thin)

        for row in ws.iter_rows():
            for cell in row:
                cell.border = border

                if cell.column == 8:
                    cell.alignment = wrap
                else:
                    cell.alignment = center

        # =========================
        # COLUMN WIDTHS
        # =========================
        widths = [6, 20, 22, 20, 30, 20, 30, 45, 25]

        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[chr(64 + i)].width = w

        # =========================
        # FILTER + FREEZE
        # =========================
        ws.auto_filter.ref = "A1:I1"
        ws.freeze_panes = "A2"

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = f'attachment; filename=activity_{date}.xlsx'

        wb.save(response)
        return response