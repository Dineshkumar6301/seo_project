from rest_framework.views import APIView
from django.http import HttpResponse
from django.db.models import Q

from openpyxl import Workbook
from openpyxl.styles import (
    Font,
    Alignment,
    PatternFill
)
from openpyxl.utils import get_column_letter

from datetime import timedelta
from django.utils.timezone import now

from activities.models import Activity
from rest_framework.permissions import IsAuthenticated


class ExportExcelAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Activity.objects.select_related(
            "user",
            "project"
        ).order_by("-date")

        export_type = request.GET.get("type")


        if export_type == "daily":

            qs = qs.filter(
                user=request.user
            )


        elif export_type == "approval":

            if not (
                request.user.is_superuser
                or request.user.is_staff
            ):

                qs = qs.filter(
                    user=request.user
        )
       
        project = request.GET.get("project")
        service = request.GET.get("service")
        task = request.GET.get("task")

    
        filter_type = (
            request.GET.get("type")
            or request.GET.get("filter")
        )

        start = (
            request.GET.get("start_date")
            or request.GET.get("start")
        )

        end = (
            request.GET.get("end_date")
            or request.GET.get("end")
        )

        # NEW OPTIONAL FILTERS
        status = request.GET.get("status")
        search = request.GET.get("search")

        if project:

            qs = qs.filter(project_id=project)

        if service:

            qs = qs.filter(service_name=service)

        if task:

            qs = qs.filter(task_type=task)

    
        if status:

            qs = qs.filter(status=status)

      
        if search:

            qs = qs.filter(
                Q(user__first_name__icontains=search)
                |
                Q(user__last_name__icontains=search)
                |
                Q(project__name__icontains=search)
                |
                Q(task_type__icontains=search)
                |
                Q(service_name__icontains=search)
            )

        today = now().date()

        if filter_type == "today":

            qs = qs.filter(date=today)

        elif filter_type == "month":

            qs = qs.filter(
                date__month=today.month,
                date__year=today.year
            )

        elif filter_type == "week":

            start_week = today - timedelta(days=today.weekday())

            end_week = start_week + timedelta(days=6)

            qs = qs.filter(
                date__range=[start_week, end_week]
            )

        elif filter_type == "year":

            qs = qs.filter(
                date__year=today.year
            )

        elif filter_type == "custom":

            if start and end:

                qs = qs.filter(
                    date__range=[start, end]
                )

        # =================================
        # CUSTOM DATE RANGE
        # =================================
        if start and end:

            qs = qs.filter(
                date__range=[start, end]
            )

        # =================================
        # WORKBOOK
        # =================================
        wb = Workbook()

        ws = wb.active

        ws.title = "SEO Report"

        # =================================
        # DYNAMIC KEYS
        # =================================
        dynamic_keys = set()

        for a in qs:

            data = a.dynamic_data or {}

            for key in data.keys():

                dynamic_keys.add(key)

        # =================================
        # PRIORITY SORT
        # =================================
        priority = [
            "keyword",
            "url",
            "submitted_url"
        ]

        dynamic_keys = list(dynamic_keys)

        dynamic_keys.sort(
            key=lambda x: (
                priority.index(x)
                if x in priority else 999,
                x
            )
        )

        # =================================
        # HEADERS
        # =================================
        headers = [
            "S.No",
            "Date",
            "Employee",
            "Project",
            "Category",
            "Service",
            "Task",
        ] + [
            k.replace("_", " ").title()
            for k in dynamic_keys
        ]

        ws.append(headers)

        # =================================
        # HEADER DESIGN
        # =================================
        header_fill = PatternFill(
            start_color="1F4E78",
            end_color="1F4E78",
            fill_type="solid"
        )

        for cell in ws[1]:

            cell.font = Font(
                bold=True,
                color="FFFFFF"
            )

            cell.fill = header_fill

            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
                wrap_text=True
            )

        # =================================
        # DATA
        # =================================
        for i, a in enumerate(qs, start=1):

            data = a.dynamic_data or {}

            # =================================
            # SUBMITTED BY
            # =================================
            employee = ""

            if a.user:

                employee = (
                    f"{a.user.first_name} "
                    f"{a.user.last_name}"
                ).strip()

                if not employee:

                    employee = a.user.email

            # =================================
            # BASE ROW
            # =================================
            row = [
                i,
                str(a.date),
                employee,
                a.project.name if a.project else "",
                getattr(a, "category", ""),
                a.service_name,
                a.task_type,
            ]

            # =================================
            # DYNAMIC VALUES
            # =================================
            for key in dynamic_keys:

                val = data.get(key, "")

                # =================================
                # MULTIPLE LINKS SUPPORT
                # =================================
                if isinstance(val, str):

                    possible_links = [
                        x.strip()
                        for x in val.replace(",", "\n").split("\n")
                        if x.strip()
                    ]

                    val = "\n".join(
                        possible_links
                    )

                row.append(val)

            ws.append(row)

            current_row = ws.max_row

            # =================================
            # CLICKABLE LINKS
            # =================================
            for idx, key in enumerate(
                dynamic_keys,
                start=8
            ):

                val = data.get(key, "")

                if isinstance(val, str):

                    first_link = (
                        val.split(",")[0]
                        .strip()
                    )

                    if (
                        first_link.startswith("http://")
                        or first_link.startswith("https://")
                    ):

                        cell = ws.cell(
                            current_row,
                            idx
                        )

                        cell.hyperlink = first_link

                        cell.style = "Hyperlink"

                        cell.alignment = Alignment(
                            wrap_text=True,
                            vertical="top"
                        )

        # =================================
        # CELL STYLING
        # =================================
        for row in ws.iter_rows():

            for cell in row:

                cell.alignment = Alignment(
                    wrap_text=True,
                    vertical="top"
                )

        # =================================
        # COLUMN WIDTH
        # =================================
        for column_cells in ws.columns:

            length = 0

            column = column_cells[0].column

            for cell in column_cells:

                try:

                    length = max(
                        length,
                        len(str(cell.value))
                    )

                except:

                    pass

            adjusted_width = min(
                length + 5,
                60
            )

            ws.column_dimensions[
                get_column_letter(column)
            ].width = adjusted_width

        # =================================
        # ROW HEIGHT
        # =================================
        for row in range(
            2,
            ws.max_row + 1
        ):

            ws.row_dimensions[row].height = 60

        # =================================
        # FREEZE HEADER
        # =================================
        ws.freeze_panes = "A2"

        # =================================
        # RESPONSE
        # =================================
        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        )

        # =================================
            # DYNAMIC FILE NAME
            # =================================
        parts = ["SEO_Report"]

        if start and end:

            parts.append(f"{start}_to_{end}")

        elif filter_type:

            parts.append(filter_type)

        if service:

            parts.append(service.replace(" ", "_"))

        if task:

            parts.append(task.replace(" ", "_"))

        if status:

            parts.append(status)

        filename = "_".join(parts) + ".xlsx"

        response[
                "Content-Disposition"
            ] = (
                f'attachment; filename="{filename}"'
            )

        wb.save(response)

        return response