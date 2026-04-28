from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q
from activities.models import Activity


class ClientDashboardAPI(APIView):

    def get(self, request):

        qs = Activity.objects.all()

        # 🔒 CLIENT RESTRICTION
        if hasattr(request.user, "client"):
            qs = qs.filter(project__client=request.user.client)

        # 🔹 PARAMS SAFE
        try:
            page = max(1, int(request.GET.get("page", 1)))
            limit = min(50, max(1, int(request.GET.get("limit", 10))))
        except:
            page, limit = 1, 10

        filter_type = request.GET.get("type")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        search = request.GET.get("search")
        service = request.GET.get("service")
        status = request.GET.get("status")
        project = request.GET.get("project")

        today = now().date()

        # 🔥 DATE FILTER (PRIORITY)
        if start_date and end_date:
            qs = qs.filter(date__range=[start_date, end_date])
        elif filter_type == "today":
            qs = qs.filter(date=today)
        elif filter_type == "week":
            qs = qs.filter(date__gte=today - timedelta(days=7))

        elif filter_type == "month":
            qs = qs.filter(date__month=today.month)
        
        elif filter_type == "year":
            qs = qs.filter(date__year=today.year)

         # 🔹 STATUS

        # 🔹 SEARCH
        if search:
            qs = qs.filter(
                Q(task_title__icontains=search) |
                Q(keyword__icontains=search) |
                Q(project__name__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        # 🔹 PROJECT
        if project:
            qs = qs.filter(project__id=project)

        # 🔹 SERVICE
        if service:
            qs = qs.filter(service__name__iexact=service.strip())

        # 🔥 KPI (FROM BASE FILTERED QS BEFORE STATUS)
        base_qs = qs

        total = base_qs.count()
        approved = base_qs.filter(status="approved").count()
        pending = base_qs.filter(status="pending").count()
        rejected = base_qs.filter(status="rejected").count()

        # 🔹 STATUS FILTER (AFTER KPI)
        if status:
            qs = qs.filter(status=status)

        # 🔹 ORDER
        qs = qs.order_by("-date")

        # 🔹 PAGINATION
        start = (page - 1) * limit
        end = start + limit

        table = list(
            qs.values(
                'id',
                'task_title',
                'keyword',
                'status',
                'proof_link',
                'date',
                'project__name',
                'user__first_name',
                'user__last_name'
            )[start:end]
        )

        total_pages = (qs.count() // limit) + (1 if qs.count() % limit else 0)

        return Response({
            "kpi": {
                "total": total,
                "approved": approved,
                "pending": pending,
                "rejected": rejected
            },
            "table": table,
            "pagination": {
                "page": page,
                "pages": total_pages
            }
        })