from rest_framework.views import APIView
from rest_framework.response import Response

from activities.models import Activity

class DailyReportAPI(APIView):

    def get(self, request):

        date = request.GET.get('date')

        activities = Activity.objects.filter(date=date, status='approved')

        return Response({
            "date": date,
            "total_tasks": activities.count()
        })