from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from activities.models import Activity

class ActivityDeleteAPI(APIView):

    def delete(self, request, pk):

        activity = get_object_or_404(Activity, pk=pk)

        if request.user.role == 'employee':
            if activity.user != request.user:
                return Response({'error': 'Not allowed'}, status=403)

        activity.delete()
        return Response({'message': 'Deleted'})