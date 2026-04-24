from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.models import User
from activities.models import Activity
from .models import Project, Service, ProjectServiceAssignment
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Count, Q



def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  
    return render(request, 'frontend/auth.html')



def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('home')

        return render(request, 'frontend/auth.html', {
            'error': 'Invalid email or password'
        })

    return redirect('home')



def register_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        mobile = request.POST.get('mobile')
        role = request.POST.get('role')

        if password != confirm_password:
            return render(request, 'frontend/auth.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'frontend/auth.html', {
                'error': 'Email already exists'
            })

        user = User.objects.create_user(email=email, password=password)

        user.first_name = first_name
        user.last_name = last_name
        user.mobile = mobile
        user.role = role
        user.save()

        login(request, user)
        return redirect('dashboard')

    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from activities.models import Activity
from projects.models import Project



@login_required(login_url='home')
def dashboard(request):

    user = request.user

    if user.role == "employee":
        return redirect("employee_dashboard")

    elif user.role == "qa":
        return redirect("qa_dashboard")

    elif user.role == "client":
        return redirect("client_dashboard")

    today = timezone.now().date()

    if user.role in ["admin", "manager"]:
        base_qs = Activity.objects.all().select_related('project', 'user')
    else:
        base_qs = Activity.objects.filter(user=user).select_related('project', 'user')

    total_projects = Project.objects.count() if user.role in ["admin", "manager"] else Project.objects.filter(owner=user).count()

    total_activities = base_qs.count()

    team_members = User.objects.exclude(role='client').count()

    pending = base_qs.filter(status='pending').count()
    approved = base_qs.filter(status='approved').count()
    rejected = base_qs.filter(status='rejected').count()

    performance = int((approved / total_activities) * 100) if total_activities else 0
    last_7_start = today - timedelta(days=6)
    prev_7_start = today - timedelta(days=13)
    prev_7_end = today - timedelta(days=7)

    last_7 = base_qs.filter(date__gte=last_7_start, date__lte=today).count()
    prev_7 = base_qs.filter(date__gte=prev_7_start, date__lte=prev_7_end).count()

    if prev_7 == 0:
        trend_pct = 100 if last_7 > 0 else 0
    else:
        trend_pct = int(((last_7 - prev_7) / prev_7) * 100)

    trend_direction = "up" if trend_pct > 0 else ("down" if trend_pct < 0 else "flat")
    tp = (
        base_qs.values('project__name')
        .annotate(c=Count('id'))
        .order_by('-c')
        .first()
    )
    top_project = tp['project__name'] if tp else "—"

    te = (
        base_qs.values('user__email')
        .annotate(c=Count('id'))
        .order_by('-c')
        .first()
    )
    top_employee = te['user__email'] if te else "—"

    risk_count = base_qs.filter(
        status='pending',
        date__lt=today - timedelta(days=2)
    ).count()

    risk_label = "High" if risk_count >= 10 else ("Medium" if risk_count >= 3 else "Low")

    spark_labels = []
    spark_data = []

    for i in range(7):
        d = last_7_start + timedelta(days=i)
        spark_labels.append(d.strftime('%d %b'))
        spark_data.append(base_qs.filter(date=d).count())
    weekday_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekday_data = [0] * 7

    for a in base_qs.filter(date__isnull=False):
        weekday_data[a.date.weekday()] += 1


    activities = base_qs.order_by('-created_at')[:5]

    context = {

        'total_projects': total_projects,
        'total_activities': total_activities,
        'team_members': team_members,
        'performance': performance,

        'pending': pending,
        'approved': approved,
        'rejected': rejected,

        'trend_pct': trend_pct,
        'trend_direction': trend_direction,
        'top_project': top_project,
        'top_employee': top_employee,
        'risk_label': risk_label,
        'risk_count': risk_count,

        'spark_labels': spark_labels,
        'spark_data': spark_data,
        'weekday_labels': weekday_labels,
        'weekday_data': weekday_data,

        'activities': activities,
    }

    return render(request, 'frontend/dashboard.html', context)


@login_required
def employee_dashboard(request):

    user = request.user

    activities = Activity.objects.filter(user=user).order_by('-date')
    total = activities.count()
    pending = activities.filter(status='pending').count()
    approved = activities.filter(status='approved').count()
    rejected = activities.filter(status='rejected').count()

    today = date.today()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]

    chart_labels = [d.strftime("%d %b") for d in last_7_days]

    day_map = (
        activities
        .exclude(date__isnull=True)
        .values('date')
        .annotate(count=Count('id'))
    )

    day_dict = {x['date']: x['count'] for x in day_map}

    chart_data = [day_dict.get(d, 0) for d in last_7_days]

    return render(request, 'frontend/employee_dashboard.html', {
        'activities': activities,
        'total': total,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })



@login_required
def qa_dashboard(request):

    activities = Activity.objects.select_related(
        'user', 'project', 'service', 'project__client'
    ).filter(status='pending')

    return render(request, 'frontend/qa_dashboard.html', {
        'activities': activities
    })

@login_required
def client_dashboard(request):

    client = request.user.client

    activities = Activity.objects.filter(
        project__client=client
    )
    chart_qs = (
        activities
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    chart_labels = [str(x['day']) for x in chart_qs]
    chart_data = [x['count'] for x in chart_qs]

    return render(request, 'frontend/client_dashboard.html', {
        'activities': activities,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    })



@login_required
def assign_services(request, project_id):

    project = Project.objects.get(id=project_id)

    users = User.objects.exclude(role='client')
    services = Service.objects.all()

    assignments = ProjectServiceAssignment.objects.filter(project=project)

    if request.method == "POST":

        user_id = request.POST.get('user')
        service_id = request.POST.get('service')

        if user_id and service_id:
            ProjectServiceAssignment.objects.get_or_create(
                project=project,
                user_id=user_id,
                service_id=service_id,
                defaults={'assigned_by': request.user}
            )

        return redirect('assign_services', project_id=project.id)

    return render(request, 'frontend/assign_services.html', {
        'project': project,
        'users': users,
        'services': services,
        'assignments': assignments
    })