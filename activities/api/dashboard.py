from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from activities.models import Activity


class ClientDashboardAPI(APIView):

    def get(self, request):

        qs = Activity.objects.all()

        # 🔒 CLIENT RESTRICTION
        if hasattr(request.user, "client"):
            qs = qs.filter(project__client=request.user.client)

        # 🔹 PARAMS SAFE
        try:
            page  = max(1, int(request.GET.get("page", 1)))
            limit = min(50, max(1, int(request.GET.get("limit", 10))))
        except (ValueError, TypeError):
            page, limit = 1, 10

        filter_type = request.GET.get("type", "").strip()
        start_date  = request.GET.get("start_date", "").strip()
        end_date    = request.GET.get("end_date", "").strip()
        search      = request.GET.get("search", "").strip()
        service     = request.GET.get("service", "").strip()
        status      = request.GET.get("status", "").strip()
        project     = request.GET.get("project", "").strip()

        today = now().date()

        # 🔥 DATE FILTER
        if start_date and end_date:
            qs = qs.filter(date__range=[start_date, end_date])
        elif filter_type == "today":
            qs = qs.filter(date=today)
        elif filter_type == "week":
            qs = qs.filter(date__gte=today - timedelta(days=7))
        elif filter_type == "month":
            qs = qs.filter(date__month=today.month, date__year=today.year)
        elif filter_type == "year":
            qs = qs.filter(date__year=today.year)

        # 🔹 SEARCH
        if search:
            qs = qs.filter(
                Q(task_title__icontains=search)      |
                Q(keyword__icontains=search)          |
                Q(project__name__icontains=search)    |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )

        # 🔹 PROJECT
        if project:
            qs = qs.filter(project__id=project)

        # 🔹 SERVICE
        if service:
            qs = qs.filter(service__name__iexact=service)

        # 🔥 KPI — computed BEFORE status filter so counts are always full
        base_qs  = qs
        total    = base_qs.count()
        approved = base_qs.filter(status="approved").count()
        pending  = base_qs.filter(status="pending").count()
        rejected = base_qs.filter(status="rejected").count()

        # ✅ CHART — daily task counts from the base filtered queryset
        chart_qs = (
            base_qs
            .annotate(day=TruncDate("date"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )
        chart_labels = [str(row["day"]) for row in chart_qs]
        chart_data   = [row["count"]    for row in chart_qs]

        # 🔹 STATUS FILTER (AFTER KPI + CHART)
        if status:
            qs = qs.filter(status=status)

        # 🔹 ORDER
        qs = qs.order_by("-date")

        # 🔹 PAGINATION
        total_count = qs.count()
        start       = (page - 1) * limit
        end         = start + limit
        total_pages = max(1, (total_count + limit - 1) // limit)   # no off-by-one

        table = list(
            qs.values(
                "id",
                "task_title",
                "keyword",
                "status",
                "proof_link",
                "date",
                "project__name",
                "user__first_name",
                "user__last_name",
            )[start:end]
        )

        # stringify dates in table so JSON serialises cleanly
        for row in table:
            if row.get("date"):
                row["date"] = str(row["date"])

        return Response({
            "kpi": {
                "total":    total,
                "approved": approved,
                "pending":  pending,
                "rejected": rejected,
            },
            "chart": {
                "labels": chart_labels,   # e.g. ["2025-04-21", "2025-04-22", ...]
                "data":   chart_data,     # e.g. [3, 7, 2, ...]
            },
            "table": table,
            "pagination": {
                "page":  page,
                "pages": total_pages,
            },
        })