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

        rows = zip(
            request.POST.getlist('project'),
            request.POST.getlist('service'),
            request.POST.getlist('task_title'),
            request.POST.getlist('planned'),
            request.POST.getlist('completed'),
            request.POST.getlist('link'),
            request.POST.getlist('remarks')
        )

        for row in rows:

            project_id = row[0]
            service_id = row[1]

            # 🔥 VALIDATION
            if not project_id or not service_id:
                continue

            Activity.objects.create(
                user=request.user,
                project_id=project_id,
                service_id=service_id,
                date=request.POST.get('date'),
                task_title=row[2],
                planned_work=row[3],
                completed_work=row[4],
                proof_link=row[5],
                remarks=row[6],
                status='pending'
            )

        return redirect('activity_daily')

    return render(request, 'frontend/activities/daily.html', {
        'projects': projects
    })




@login_required
def activity_approval(request):

    status = request.GET.get('status', 'pending')
    date_filter = request.GET.get('date', 'today')
    search = request.GET.get('search', '')
    project_id = request.GET.get('project', '')

    today = timezone.now().date()

    queryset = Activity.objects.select_related(
        'user', 'project', 'service'
    )

    # 🔥 DATE FILTER
    if date_filter == "today":
        queryset = queryset.filter(date=today)

    elif date_filter == "week":
        queryset = queryset.filter(date__gte=today - timedelta(days=7))

    elif date_filter == "month":
        queryset = queryset.filter(date__month=today.month)

    elif date_filter == "year":
        queryset = queryset.filter(date__year=today.year)

    # 🔥 SEARCH (EMPLOYEE EMAIL)
    if search:
        queryset = queryset.filter(user__email__icontains=search)

    # 🔥 PROJECT FILTER
    if project_id:
        queryset = queryset.filter(project_id=project_id)

    # 🔥 COUNTS
    counts = queryset.values('status').annotate(count=Count('id'))
    count_map = {i['status']: i['count'] for i in counts}

    pending_count = count_map.get('pending', 0)
    approved_count = count_map.get('approved', 0)
    rejected_count = count_map.get('rejected', 0)

    # 🔥 EXPORT EXCEL
    if request.GET.get('export') == "excel":

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Activity Report"

        ws.append(["User", "Project", "Task", "Status", "Date"])

        for a in queryset:
            ws.append([
                a.user.email,
                a.project.name,
                a.task_title,
                a.status,
                str(a.date)
            ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=report.xlsx'

        wb.save(response)
        return response

    activities = queryset.filter(status=status).order_by('-created_at')

    projects = Project.objects.all()
    profile =Profile.objects.filter(user=request.user).first()

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