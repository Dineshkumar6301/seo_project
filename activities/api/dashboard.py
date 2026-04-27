from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from activities.models import Activity


class ClientDashboardAPI(APIView):

    def get(self, request):

        # 🔹 BASE QUERY
        qs = Activity.objects.filter(
            project__client=request.user.client
        )

        # 🔹 FILTER PARAMS
        filter_type = request.GET.get("type", "all")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        search = request.GET.get("search")
        service = request.GET.get("service")
        order = request.GET.get("order", "-date")

        today = now().date()

        # 🔹 DATE FILTER (priority)
        if start_date and end_date:
            qs = qs.filter(date__range=[start_date, end_date])

        elif filter_type == "today":
            qs = qs.filter(date=today)

        elif filter_type == "week":
            qs = qs.filter(date__gte=today - timedelta(days=7))

        elif filter_type == "month":
            qs = qs.filter(date__month=today.month)

        # 🔹 SEARCH FILTER
        if search:
            qs = qs.filter(
                Q(task_title__icontains=search) |
                Q(project__name__icontains=search)
            )

        # 🔹 SERVICE FILTER
        if service:
            qs = qs.filter(service__name__iexact=service)

        # 🔹 ORDERING
        qs = qs.order_by(order)

        # 🔹 SERVICES (dynamic dropdown)
        services = list(
            qs.values_list("service__name", flat=True).distinct()
        )

        # 🔹 KPI (single-pass counts)
        total = qs.count()
        approved = qs.filter(status="approved").count()
        pending = qs.filter(status="pending").count()
        rejected = qs.filter(status="rejected").count()

        completion_rate = (approved / total * 100) if total else 0

        # 🔹 CHART (last 30 days only)
        chart_qs = (
            qs.annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('-day')[:30]
        )

        chart_qs = list(chart_qs)[::-1]  # reverse for frontend

        chart_labels = [str(x['day']) for x in chart_qs]
        chart_data = [x['count'] for x in chart_qs]

        # 🔥 PAGINATION (dynamic limit)
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))

        total_count = qs.count()
        total_pages = (total_count // limit) + (1 if total_count % limit else 0)

        start = (page - 1) * limit
        end = start + limit

        table = list(qs.values(
            'task_title',
            'status',
            'proof_link',
            'date',
            'project__name'
        )[start:end])

        # 🔹 RESPONSE
        return Response({
            "kpi": {
                "total": total,
                "approved": approved,
                "pending": pending,
                "rejected": rejected,
                "completion_rate": round(completion_rate, 2)
            },
            "chart": {
                "labels": chart_labels,
                "data": chart_data
            },
            "table": table,
            "services": services,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": total_pages
            }
        })