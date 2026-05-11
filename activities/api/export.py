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
from clients.models import Client


class ExportExcelAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        qs = Activity.objects.select_related(
            "user",
            "project"
        ).order_by("-date")

        export_type = (
            request.GET.get("export_type")
            or request.GET.get("type")
        )

        try:

            client = Client.objects.get(
                user=request.user
            )

            qs = qs.filter(
                project__client=client
            )

        except Client.DoesNotExist:

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
                |
                Q(category__icontains=search)
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

            start_week = (
                today - timedelta(
                    days=today.weekday()
                )
            )

            end_week = (
                start_week + timedelta(days=6)
            )

            qs = qs.filter(
                date__range=[
                    start_week,
                    end_week
                ]
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

        if start and end:

            qs = qs.filter(
                date__range=[start, end]
            )

        wb = Workbook()

        ws = wb.active

        ws.title = "SEO Report"

        headers = [
            "S.No",
            "Date",
            "Employee",
            "Project",
            "Category",
            "Service",
            "Task",
            "Keyword",
            "Submitted URLs",
            "Target URLs",
            "Proof / Other Data",
        ]

        ws.append(headers)


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


        for i, a in enumerate(qs, start=1):

            data = a.dynamic_data or {}

            employee = ""

            if a.user:

                employee = (
                    f"{a.user.first_name} "
                    f"{a.user.last_name}"
                ).strip()

                if not employee:

                    employee = a.user.email


            keyword = (
                data.get("keyword")
                or data.get("KEYWORD")
                or data.get("Keyword")
                or ""
            )


            submitted_urls = (
                data.get("submitted_url")
                or data.get("submitted_urls")
                or data.get("SUBMITTED_URL")
                or data.get("Submitted_url")
                or ""
            )

            if isinstance(submitted_urls, str):

                submitted_urls = "\n".join([
                    x.strip()
                    for x in submitted_urls
                    .replace(",", "\n")
                    .split("\n")
                    if x.strip()
                ])

        

            target_urls = (
                data.get("target_url")
                or data.get("target_urls")
                or data.get("TARGET_URL")
                or data.get("Target_url")
                or data.get("TARGET_URL")
                or ""
            )

            if isinstance(target_urls, str):

                target_urls = "\n".join([
                    x.strip()
                    for x in target_urls
                    .replace(",", "\n")
                    .split("\n")
                    if x.strip()
                ])

            other_data_parts = []

            for key, value in data.items():

                lower_key = str(key).lower()

            
                if lower_key in [
                    "keyword",
                    "submitted_url",
                    "submitted_urls",
                    "target_url",
                    "target_urls"
                ]:
                    continue

                
                if (
                    value is None or
                    value == ""
                ):
                    continue

                
                if isinstance(value, list):

                    value = ", ".join(
                        map(str, value)
                    )

                other_data_parts.append(
                    f"{key}: {value}"
                )

            other_data = "\n".join(
                other_data_parts
            )

            row = [
                i,
                str(a.date),
                employee,
                a.project.name if a.project else "",
                getattr(a, "category", ""),
                a.service_name,
                a.task_type,
                keyword,
                submitted_urls,
                target_urls,
                other_data,
            ]

            ws.append(row)

            current_row = ws.max_row


            if submitted_urls:

                first_link = (
                    submitted_urls
                    .split("\n")[0]
                    .strip()
                )

                if first_link.startswith(
                    ("http://", "https://")
                ):

                    cell = ws.cell(
                        current_row,
                        9
                    )

                    cell.hyperlink = first_link
                    cell.style = "Hyperlink"


            if target_urls:

                first_link = (
                    target_urls
                    .split("\n")[0]
                    .strip()
                )

                if first_link.startswith(
                    ("http://", "https://")
                ):

                    cell = ws.cell(
                        current_row,
                        10
                    )

                    cell.hyperlink = first_link
                    cell.style = "Hyperlink"



        for row in ws.iter_rows():

            for cell in row:

                cell.alignment = Alignment(
                    wrap_text=True,
                    vertical="top"
                )


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

  

        for row in range(
            2,
            ws.max_row + 1
        ):

            ws.row_dimensions[row].height = 60


        ws.freeze_panes = "A2"


        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            )
        )

        parts = ["Report"]

        if start and end:

            parts.append(
                f"{start}_to_{end}"
            )

        elif filter_type:

            parts.append(filter_type)

        if service:

            parts.append(
                service.replace(" ", "_")
            )

        if task:

            parts.append(
                task.replace(" ", "_")
            )

        if status:

            parts.append(status)

        filename = (
            "_".join(parts)
            + ".xlsx"
        )

        response[
            "Content-Disposition"
        ] = (
            f'attachment; filename="{filename}"'
        )

        wb.save(response)

        return response