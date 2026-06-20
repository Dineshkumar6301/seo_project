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



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from clients.models import (
    Client,
    ClientOnboarding
)
from django.shortcuts import render, redirect, get_object_or_404
@login_required
def client_onboarding(
    request,
    client_id=None
):

    is_client = hasattr(
        request.user,
        "client"
    )

    if is_client:

        client = request.user.client

    else:

        client = get_object_or_404(
            Client,
            id=client_id
        )

    onboarding, created = (
        ClientOnboarding.objects.get_or_create(
            client=client
        )
    )
    # Only Admin can edit

    if request.method == "POST" and not is_client:

        onboarding.business_name = request.POST.get(
            "business_name", ""
        )

        onboarding.website = request.POST.get(
            "website", ""
        )

        onboarding.business_category = request.POST.get(
            "business_category", ""
        )

        onboarding.service_areas = request.POST.get(
            "service_areas", ""
        )

        onboarding.target_audience = request.POST.get(
            "target_audience", ""
        )

        onboarding.competitors = request.POST.get(
            "competitors", ""
        )

        onboarding.business_description = request.POST.get(
            "business_description", ""
        )

        onboarding.hosting_provider = request.POST.get("hosting_provider", "")
        onboarding.hosting_notes = request.POST.get("hosting_notes", "")

        onboarding.domain_provider = request.POST.get("domain_provider", "")
        onboarding.domain_notes = request.POST.get("domain_notes", "")

        onboarding.ga_property_id = request.POST.get("ga_property_id", "")
        onboarding.ga_notes = request.POST.get("ga_notes", "")

        onboarding.gsc_property = request.POST.get("gsc_property", "")
        onboarding.gsc_notes = request.POST.get("gsc_notes", "")

        onboarding.google_ads_customer_id = request.POST.get("google_ads_customer_id", "")
        onboarding.google_ads_notes = request.POST.get("google_ads_notes", "")

        onboarding.meta_business_id = request.POST.get("meta_business_id", "")
        onboarding.meta_notes = request.POST.get("meta_notes", "")

        onboarding.youtube_channel_name = request.POST.get("youtube_channel_name", "")
        onboarding.youtube_access_email = request.POST.get("youtube_access_email", "")
        onboarding.youtube_notes = request.POST.get("youtube_notes", "")

        onboarding.facebook_page = request.POST.get("facebook_page", "")
        onboarding.instagram_handle = request.POST.get("instagram_handle", "")
        onboarding.linkedin_page = request.POST.get("linkedin_page", "")
        onboarding.twitter_handle = request.POST.get("twitter_handle", "")
        onboarding.social_notes = request.POST.get("social_notes", "")

        onboarding.kpi_defined = (
            "kpi_defined" in request.POST
        )

        onboarding.deliverables_defined = (
            "deliverables_defined" in request.POST
        )

        onboarding.reporting_setup = (
            "reporting_setup" in request.POST
        )

        onboarding.notes = request.POST.get(
            "notes", ""
        )

        onboarding.save()

        messages.success(
            request,
            "Onboarding Updated Successfully."
        )

        return redirect(
            request.path
        )

    completed_steps = sum([

        onboarding.hosting_access,

        onboarding.domain_access,

        onboarding.ga_access,

        onboarding.gsc_access,

        

        onboarding.google_ads_access,

        onboarding.meta_access,

        onboarding.youtube_access,

        onboarding.social_media_access,

        onboarding.team_assigned,

        onboarding.kpi_defined,

        onboarding.deliverables_defined,

        onboarding.reporting_setup,
    ])

    progress = int(
        (completed_steps / 12) * 100
    )

    return render(

        request,

        "frontend/clients/onboarding.html",

        {

            "client": client,

            "onboarding": onboarding,

            "progress": progress,

            "is_client": is_client,
        }
    )