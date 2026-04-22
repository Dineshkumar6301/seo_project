from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from activities.models import Activity
from activities.serializers import ActivitySerializer

class ActivityListAPI(APIView):

    def get(self, request):

        activities = Activity.objects.all()

        # Role filtering
        if request.user.role == 'employee':
            activities = activities.filter(user=request.user)

        elif request.user.role == 'client':
            activities = activities.filter(
                project__client__user=request.user,
                status='approved'
            )

        # Filters
        date = request.GET.get('date')
        project = request.GET.get('project')
        status_val = request.GET.get('status')

        if date:
            activities = activities.filter(date=date)

        if project:
            activities = activities.filter(project_id=project)

        if status_val:
            activities = activities.filter(status=status_val)

        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)