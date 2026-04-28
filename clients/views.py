from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer
from accounts.permissions import IsAdminOrManager


class ClientCreateAPI(APIView):
    permission_classes = [IsAdminOrManager]

    def post(self, request):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Client created"}, status=201)

        return Response(serializer.errors, status=400)
    

from django.shortcuts import render, redirect
from .models import Client

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'frontend/clients/list.html', {'clients': clients})

