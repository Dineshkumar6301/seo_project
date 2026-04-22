# activities/api/filter.py

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta
from activities.models import Activity

class ActivityFilterAPI(APIView):

    def get(self, request):

        filter_type = request.GET.get("type")

        qs = Activity.objects.all()

        today = now().date()

        if filter_type == "today":
            qs = qs.filter(date=today)

        elif filter_type == "week":
            qs = qs.filter(date__gte=today - timedelta(days=7))

        elif filter_type == "month":
            qs = qs.filter(date__month=today.month)

        data = list(qs.values(
            'id',
            'task_title',
            'status',
            'date',
            'project__name'
        ))

        return Response(data)