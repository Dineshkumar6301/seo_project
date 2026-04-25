from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.http import HttpResponse

from datetime import timedelta, datetime

from projects.models import Project
from activities.models import Activity
from accounts.models import User, Profile

from openpyxl import Workbook
import openpyxl


@login_required
def activity_daily(request):

    projects = Project.objects.all()

    if request.method == "POST":

        projects_list = request.POST.getlist('project')
        services_list = request.POST.getlist('service')
        task_titles = request.POST.getlist('task_title')
        planned_list = request.POST.getlist('planned')
        completed_list = request.POST.getlist('completed')
        remarks_list = request.POST.getlist('remarks')

        total_rows = len(projects_list)

        for i in range(total_rows):

            project_id = projects_list[i]
            service_id = services_list[i]

            if not project_id or not service_id:
                continue

            # 🔥 GET MULTIPLE LINKS PER ROW
            links = request.POST.getlist(f'link_{i}')
            proof_text = "\n".join([l for l in links if l.strip()])

            Activity.objects.create(
                user=request.user,
                project_id=project_id,
                service_id=service_id,
                date=request.POST.get('date'),
                task_title=task_titles[i],
                planned_work=planned_list[i],
                completed_work=completed_list[i],
                proof_link=proof_text,
                remarks=remarks_list[i],
                status='pending'
            )

        return redirect('activity_daily')

    return render(request, 'frontend/activities/daily.html', {
        'projects': projects
    })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.http import HttpResponse

import openpyxl

from activities.models import Activity
from projects.models import Project
from accounts.models import Profile


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Count
from django.http import HttpResponse

import openpyxl

from activities.models import Activity
from projects.models import Project
from accounts.models import Profile


@login_required
def activity_approval(request):

    status = request.GET.get('status', 'pending')
    date_filter = request.GET.get('date', 'all')  # ✅ default = all
    search = request.GET.get('search', '')
    project_id = request.GET.get('project', '')

    today = timezone.now().date()

    queryset = Activity.objects.select_related(
        'user', 'project', 'service'
    )

    # =========================
    # 🔥 DATE FILTER
    # =========================
    if date_filter == "today":
        queryset = queryset.filter(date=today)

    elif date_filter == "week":
        queryset = queryset.filter(date__gte=today - timedelta(days=6))

    elif date_filter == "month":
        queryset = queryset.filter(
            date__month=today.month,
            date__year=today.year
        )

    elif date_filter == "year":
        queryset = queryset.filter(date__year=today.year)

    elif date_filter == "custom":
        selected_date = request.GET.get("selected_date")

        if selected_date:
            try:
                selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
                queryset = queryset.filter(date=selected_date)
            except:
                pass  # ignore invalid date

    elif date_filter == "all":
        pass

    # =========================
    # 🔥 SEARCH (EMAIL)
    # =========================
    if search:
        queryset = queryset.filter(user__email__icontains=search)

    # =========================
    # 🔥 PROJECT FILTER
    # =========================
    if project_id:
        queryset = queryset.filter(project_id=project_id)

    # =========================
    # 🔥 COUNTS (BEFORE STATUS FILTER)
    # =========================
    counts = queryset.values('status').annotate(count=Count('id'))
    count_map = {i['status']: i['count'] for i in counts}

    pending_count = count_map.get('pending', 0)
    approved_count = count_map.get('approved', 0)
    rejected_count = count_map.get('rejected', 0)

    # =========================
    # 🔥 EXPORT EXCEL
    # =========================
    if request.GET.get('export') == "excel":

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Activity Report"

        ws.append([
            "User",
            "Project",
            "Service",
            "Task",
            "Planned",
            "Completed",
            "Proof Links",
            "Status",
            "Date"
        ])

        for a in queryset:
            ws.append([
                a.user.email,
                a.project.name,
                a.service.name if a.service else "",
                a.task_title,
                a.planned_work,
                a.completed_work,
                a.proof_link or "",
                a.status,
                str(a.date)
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=activity_report.xlsx'

        wb.save(response)
        return response

    # =========================
    # 🔥 STATUS FILTER
    # =========================
    activities = queryset.filter(status=status).order_by('-created_at')

    # =========================
    # 🔥 EXTRA DATA
    # =========================
    projects = Project.objects.all()
    profile = Profile.objects.filter(user=request.user).first()

    return render(request, 'frontend/activities/approval.html', {
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
    })
@login_required
def activity_reports(request):

    activities = Activity.objects.select_related(
        'user', 'project', 'service'
    ).order_by('-date')

    return render(request, 'frontend/activities/reports.html', {
        'activities': activities
    })



def export_report(request):

    now = datetime.now()

    activities = Activity.objects.filter(
        date__month=now.month,
        date__year=now.year
    ).select_related('project', 'user', 'service')

    wb = Workbook()


    ws = wb.active
    ws.title = "Activities"

    ws.append(["Project", "Employee", "Service", "Task", "Status", "Date"])

    for a in activities:
        ws.append([
            a.project.name if a.project else "",
            a.user.email if a.user else "",
            a.service.name if a.service else "",
            a.task_title,
            a.status,
            str(a.date)
        ])


    summary = wb.create_sheet("Summary")

    total = activities.count()
    approved = activities.filter(status='approved').count()
    pending = activities.filter(status='pending').count()
    rejected = activities.filter(status='rejected').count()

    performance = int((approved / total) * 100) if total else 0

    summary.append(["Metric", "Value"])
    summary.append(["Total Tasks", total])
    summary.append(["Approved", approved])
    summary.append(["Pending", pending])
    summary.append(["Rejected", rejected])
    summary.append(["Performance %", performance])

    top_project = (
        activities.values('project__name')
        .annotate(c=Count('id'))
        .order_by('-c')
        .first()
    )

    summary.append([])
    summary.append(["Top Project", top_project['project__name'] if top_project else "—"])

    top_emp = (
        activities.values('user__email')
        .annotate(c=Count('id'))
        .order_by('-c')
        .first()
    )

    summary.append(["Top Employee", top_emp['user__email'] if top_emp else "—"])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=DMOS_Report.xlsx'

    wb.save(response)
    return response