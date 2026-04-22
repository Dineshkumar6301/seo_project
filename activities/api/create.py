from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from activities.models import Activity
from activities.serializers import ActivitySerializer

class ActivityCreateAPI(APIView):

    def post(self, request):
        serializer = ActivitySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)