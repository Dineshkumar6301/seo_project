# activities/api/activity.py

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from activities.models import Activity
from activities.serializers import ActivitySerializer