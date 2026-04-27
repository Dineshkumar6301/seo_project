from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from activities.models import Activity


class ClientDashboardAPI(APIView):

    def get(self, request):

        filter_type = request.GET.get("type", "all")

        qs = Activity.objects.filter(
            project__client=request.user.client
        )

        today = now().date()

        if filter_type == "today":
            qs = qs.filter(date=today)

        elif filter_type == "week":
            qs = qs.filter(date__gte=today - timedelta(days=7))

        elif filter_type == "month":
            qs = qs.filter(date__month=today.month)

        # KPI
        total = qs.count()
        approved = qs.filter(status="approved").count()
        pending = qs.filter(status="pending").count()
        rejected = qs.filter(status="rejected").count()

        # CHART
        chart_qs = (
            qs.annotate(day=TruncDate('created_at'))   # SAFE FIELD
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        chart_labels = [str(x['day']) for x in chart_qs]
        chart_data = [x['count'] for x in chart_qs]

        # TABLE
        table = list(qs.values(
            'task_title',
            'status',
            'proof_link', 
            'date',
            'project__name'
        ))

        return Response({
            "kpi": {
                "total": total,
                "approved": approved,
                "pending": pending,
                "rejected": rejected
            },
            "chart": {
                "labels": chart_labels,
                "data": chart_data
            },
            "table": table
        })