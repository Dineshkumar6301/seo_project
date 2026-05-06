from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from activities.models import Activity


class ActivityDeleteAPI(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        activity = get_object_or_404(Activity, pk=pk)

        # 🔒 Employee can delete only own data
        if hasattr(request.user, "role") and request.user.role == 'employee':
            if activity.user != request.user:
                return Response({'error': 'Not allowed'}, status=403)

        activity.delete()

        return Response({
            'message': 'Deleted successfully'
        })