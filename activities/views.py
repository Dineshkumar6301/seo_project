from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse

from datetime import timedelta, datetime

from projects.models import Project
from activities.models import Activity
from accounts.models import Profile

from openpyxl import Workbook
from openpyxl.styles import Alignment
import openpyxl

@login_required
def activity_daily(request):

    projects = Project.objects.all()

    return render(request, 'frontend/activities/daily.html', {
        'projects': projects
    })

from django.db.models import Q
from django.db.models import Q, Count
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from datetime import timedelta, datetime

import openpyxl

from openpyxl.styles import (
    Alignment,
    Font,
    Border,
    Side,
    PatternFill
)

from activities.models import Activity
from projects.models import Project



# =====================================
# APPROVAL DASHBOARD
# =====================================
@login_required
def activity_approval(request):

    status = request.GET.get(
        'status',
        'pending'
    )

    date_filter = request.GET.get(
        'date',
        'all'
    )

    search = request.GET.get(
        'search',
        ''
    )

    project_id = request.GET.get(
        'project',
        ''
    )

    today = timezone.now().date()

    # =====================================
    # QUERYSET
    # =====================================
    queryset = Activity.objects.select_related(
        'user',
        'project'
    )

    # =====================================
    # DATE FILTERS
    # =====================================
    if date_filter == "today":

        queryset = queryset.filter(
            date=today
        )

    elif date_filter == "week":

        queryset = queryset.filter(
            date__gte=today - timedelta(days=6)
        )

    elif date_filter == "month":

        queryset = queryset.filter(
            date__month=today.month,
            date__year=today.year
        )

    elif date_filter == "year":

        queryset = queryset.filter(
            date__year=today.year
        )

    elif date_filter == "custom":

        selected_date = request.GET.get(
            "selected_date"
        )

        if selected_date:

            try:

                selected_date = datetime.strptime(
                    selected_date,
                    "%Y-%m-%d"
                ).date()

                queryset = queryset.filter(
                    date=selected_date
                )

            except:

                pass

    # =====================================
    # SEARCH
    # =====================================
    if search:

        search = search.strip()

    queryset = queryset.filter(

        Q(user__email__icontains=search)

        |

        Q(user__first_name__icontains=search)

        |

        Q(user__last_name__icontains=search)

        |

        Q(project__name__icontains=search)

        |

        Q(category__iregex=rf".*{search}.*")

        |

        Q(service_name__iregex=rf".*{search}.*")

        |

        Q(task_type__iregex=rf".*{search}.*")

    )
    # =====================================
    # PROJECT FILTER
    # =====================================
    if project_id:

        queryset = queryset.filter(
            project_id=project_id
        )

    # =====================================
    # COUNTS
    # =====================================
    counts = queryset.values(
        'status'
    ).annotate(
        count=Count('id')
    )

    count_map = {
        i['status']: i['count']
        for i in counts
    }

    pending_count = count_map.get(
        'pending',
        0
    )

    approved_count = count_map.get(
        'approved',
        0
    )

    rejected_count = count_map.get(
        'rejected',
        0
    )

    # =====================================
    # EXPORT EXCEL
    # =====================================
    if request.GET.get('export') == "excel":

        wb = openpyxl.Workbook()

        ws = wb.active

        ws.title = "Activity Report"

        # =====================================
        # HEADERS
        # =====================================
        headers = [

            "S.No",

            "Project",

            "Employee",

            "Category",

            "Service",

            "Task",

            "Keyword",

            "Submitted URL",

            "Status",

            "Date"
        ]

        ws.append(headers)

        # =====================================
        # STYLES
        # =====================================
        header_font = Font(
            bold=True,
            color="FFFFFF"
        )

        header_fill = PatternFill(
            start_color="4F46E5",
            fill_type="solid"
        )

        center = Alignment(
            horizontal="center",
            vertical="center"
        )

        wrap = Alignment(
            wrap_text=True,
            vertical="top"
        )

        thin = Side(style="thin")

        border = Border(
            left=thin,
            right=thin,
            top=thin,
            bottom=thin
        )

        # =====================================
        # HEADER STYLE
        # =====================================
        for cell in ws[1]:

            cell.font = header_font

            cell.fill = header_fill

            cell.alignment = center

            cell.border = border

        # =====================================
        # DATA
        # =====================================
        row_num = 2

        serial = 1

        for a in queryset.order_by('-created_at'):

            dynamic = a.dynamic_data or {}

            keyword = dynamic.get(
                "keyword",
                ""
            )

            submitted_url = (

                dynamic.get("submitted_url")

                or

                dynamic.get("url")

                or

                dynamic.get("proof_link")

                or

                ""
            )

            links = [

                l.strip()

                for l in str(
                    submitted_url
                ).split(",")

                if l.strip()

            ] or [""]

            start_row = row_num

            for i, link in enumerate(links):

                ws.cell(
                    row=row_num,
                    column=1,
                    value=serial if i == 0 else ""
                )

                ws.cell(
                    row=row_num,
                    column=2,
                    value=a.project.name
                    if i == 0 else ""
                )

                ws.cell(
                    row=row_num,
                    column=3,
                    value=a.user.email
                    if i == 0 else ""
                )

                ws.cell(
                    row=row_num,
                    column=4,
                    value=a.category
                    if i == 0 else ""
                )

                ws.cell(
                    row=row_num,
                    column=5,
                    value=a.service_name
                    if i == 0 else ""
                )

                ws.cell(
                    row=row_num,
                    column=6,
                    value=a.task_type
                    if i == 0 else ""
                )

                ws.cell(
                    row=row_num,
                    column=7,
                    value=keyword
                    if i == 0 else ""
                )

                ws.cell(
                    row=row_num,
                    column=8,
                    value=link
                )

                ws.cell(
                    row=row_num,
                    column=9,
                    value=a.status
                    if i == 0 else ""
                )

                ws.cell(
                    row=row_num,
                    column=10,
                    value=str(a.date)
                    if i == 0 else ""
                )

                # HYPERLINK
                if link:

                    cell = ws.cell(
                        row=row_num,
                        column=8
                    )

                    cell.hyperlink = link

                    cell.style = "Hyperlink"

                # BORDER + ALIGNMENT
                for col in range(1, 11):

                    c = ws.cell(
                        row=row_num,
                        column=col
                    )

                    c.border = border

                    if col == 8:

                        c.alignment = wrap

                    else:

                        c.alignment = center

                row_num += 1

            end_row = row_num - 1

            # =====================================
            # MERGE CELLS
            # =====================================
            if end_row > start_row:

                for col in [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    9,
                    10
                ]:

                    ws.merge_cells(

                        start_row=start_row,

                        start_column=col,

                        end_row=end_row,

                        end_column=col
                    )

            # =====================================
            # STATUS COLORS
            # =====================================
            status_cell = ws.cell(
                row=start_row,
                column=9
            )

            if a.status == "approved":

                status_cell.fill = PatternFill(
                    start_color="D1FAE5",
                    fill_type="solid"
                )

            elif a.status == "pending":

                status_cell.fill = PatternFill(
                    start_color="FEF3C7",
                    fill_type="solid"
                )

            elif a.status == "rejected":

                status_cell.fill = PatternFill(
                    start_color="FEE2E2",
                    fill_type="solid"
                )

            serial += 1

        # =====================================
        # COLUMN WIDTHS
        # =====================================
        widths = [

            8,
            24,
            28,
            18,
            22,
            24,
            24,
            55,
            16,
            16
        ]

        for i, w in enumerate(
            widths,
            start=1
        ):

            ws.column_dimensions[
                chr(64 + i)
            ].width = w

        # =====================================
        # FILTER + FREEZE
        # =====================================
        ws.auto_filter.ref = "A1:J1"

        ws.freeze_panes = "A2"

        # =====================================
        # RESPONSE
        # =====================================
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        response[
            'Content-Disposition'
        ] = 'attachment; filename=activity_report.xlsx'

        wb.save(response)

        return response

    # =====================================
    # ACTIVITIES
    # =====================================
    activities = queryset.filter(
        status=status
    ).order_by('-created_at')

    projects = Project.objects.all()

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    # =====================================
    # RENDER
    # =====================================
    return render(

        request,

        'frontend/activities/approval.html',

        {

            'activities': activities,

            'projects': projects,

            'current_status': status,

            'date_filter': date_filter,

            'pending_count': pending_count,

            'approved_count': approved_count,

            'rejected_count': rejected_count,

            'search': search,

            'selected_project': project_id,

            'profile': profile
        }
    )


# =====================================
# REPORT PAGE
# =====================================
@login_required
def activity_reports(request):

    activities = Activity.objects.select_related(
        'user',
        'project'
    ).order_by('-date')

    return render(

        request,

        'frontend/activities/reports.html',

        {
            'activities': activities
        }
    )

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side
from django.http import HttpResponse
from datetime import datetime

from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill

from .models import Activity


@login_required
def export_report(request):

    now = datetime.now()

    # =====================================
    # ACTIVITIES
    # =====================================
    activities = Activity.objects.filter(

        date__month=now.month,
        date__year=now.year

    ).select_related(

        'project',
        'user'

    )

    # =====================================
    # WORKBOOK
    # =====================================
    wb = Workbook()

    ws = wb.active

    ws.title = "Activities"

    # =====================================
    # HEADERS
    # =====================================
    headers = [

        "S.No",

        "Project",

        "Employee",

        "Category",

        "Service",

        "Task",

        "Keyword",

        "Submitted URL",

        "Status",

        "Date"
    ]

    ws.append(headers)

    # =====================================
    # STYLES
    # =====================================
    header_font = Font(
        bold=True,
        color="FFFFFF"
    )

    header_fill = PatternFill(
        start_color="4F46E5",
        fill_type="solid"
    )

    center_align = Alignment(
        horizontal="center",
        vertical="center"
    )

    wrap_align = Alignment(
        wrap_text=True,
        vertical="top"
    )

    # =====================================
    # HEADER STYLE
    # =====================================
    for cell in ws[1]:

        cell.font = header_font

        cell.fill = header_fill

        cell.alignment = center_align

    # =====================================
    # ROWS
    # =====================================
    row_num = 2

    serial = 1

    for a in activities:

        dynamic = a.dynamic_data or {}

        keyword = dynamic.get(
            "keyword",
            ""
        )

        submitted_url = (

            dynamic.get("submitted_url")

            or

            dynamic.get("proof_link")

            or

            dynamic.get("url")

            or

            ""
        )

        links = [

            l.strip()

            for l in str(submitted_url).split(",")

            if l.strip()

        ] or [""]

        start_row = row_num

        for i, link in enumerate(links):

            ws.cell(
                row=row_num,
                column=1,
                value=serial if i == 0 else ""
            )

            ws.cell(
                row=row_num,
                column=2,
                value=a.project.name if i == 0 else ""
            )

            ws.cell(
                row=row_num,
                column=3,
                value=a.user.email if i == 0 else ""
            )

            ws.cell(
                row=row_num,
                column=4,
                value=a.category if i == 0 else ""
            )

            ws.cell(
                row=row_num,
                column=5,
                value=a.service_name if i == 0 else ""
            )

            ws.cell(
                row=row_num,
                column=6,
                value=a.task_type if i == 0 else ""
            )

            ws.cell(
                row=row_num,
                column=7,
                value=keyword if i == 0 else ""
            )

            ws.cell(
                row=row_num,
                column=8,
                value=link
            )

            ws.cell(
                row=row_num,
                column=9,
                value=a.status if i == 0 else ""
            )

            ws.cell(
                row=row_num,
                column=10,
                value=str(a.date) if i == 0 else ""
            )

            # CLICKABLE LINK
            if link:

                cell = ws.cell(
                    row=row_num,
                    column=8
                )

                cell.hyperlink = link

                cell.style = "Hyperlink"

            row_num += 1

        end_row = row_num - 1

        # =====================================
        # MERGE
        # =====================================
        if end_row > start_row:

            for col in [
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                9,
                10
            ]:

                ws.merge_cells(

                    start_row=start_row,

                    start_column=col,

                    end_row=end_row,

                    end_column=col
                )

        serial += 1

    # =====================================
    # BORDER
    # =====================================
    thin = Side(style="thin")

    border = Border(
        left=thin,
        right=thin,
        top=thin,
        bottom=thin
    )

    for row in ws.iter_rows():

        for cell in row:

            cell.border = border

            if cell.column == 8:

                cell.alignment = wrap_align

            else:

                cell.alignment = center_align

    # =====================================
    # STATUS COLORS
    # =====================================
    for row in ws.iter_rows(min_row=2):

        status_cell = row[8]

        if status_cell.value == "approved":

            status_cell.fill = PatternFill(
                start_color="D1FAE5",
                fill_type="solid"
            )

        elif status_cell.value == "pending":

            status_cell.fill = PatternFill(
                start_color="FEF3C7",
                fill_type="solid"
            )

        elif status_cell.value == "rejected":

            status_cell.fill = PatternFill(
                start_color="FEE2E2",
                fill_type="solid"
            )

    # =====================================
    # WIDTHS
    # =====================================
    widths = [
        8,
        24,
        28,
        20,
        20,
        28,
        20,
        50,
        16,
        16
    ]

    for i, w in enumerate(widths, start=1):

        ws.column_dimensions[
            chr(64 + i)
        ].width = w

    # =====================================
    # FILTER
    # =====================================
    ws.auto_filter.ref = "A1:J1"

    ws.freeze_panes = "A2"

    # =====================================
    # SUMMARY SHEET
    # =====================================
    summary = wb.create_sheet("Summary")

    total = activities.count()

    approved = activities.filter(
        status='approved'
    ).count()

    pending = activities.filter(
        status='pending'
    ).count()

    rejected = activities.filter(
        status='rejected'
    ).count()

    performance = int(
        (approved / total) * 100
    ) if total else 0

    summary.append([
        "Metric",
        "Value"
    ])

    summary.append([
        "Total Tasks",
        total
    ])

    summary.append([
        "Approved",
        approved
    ])

    summary.append([
        "Pending",
        pending
    ])

    summary.append([
        "Rejected",
        rejected
    ])

    summary.append([
        "Performance %",
        performance
    ])

    for cell in summary[1]:

        cell.font = Font(bold=True)

        cell.alignment = center_align

    # =====================================
    # RESPONSE
    # =====================================
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=DMOS_Report.xlsx'

    wb.save(response)

    return response