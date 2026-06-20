from django.db import models
from django.conf import settings

class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    phone = models.CharField(
        max_length=20,
        blank=True
    )

    contact_person = models.CharField(
        max_length=255,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name or self.user.username
        

from django.db import models


class ClientOnboarding(models.Model):

    client = models.OneToOneField(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='onboarding'
    )

    # ==========================================
    # BUSINESS INFORMATION
    # ==========================================

    business_name = models.CharField(
        max_length=255,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    business_category = models.CharField(
        max_length=255,
        blank=True
    )

    target_audience = models.TextField(
        blank=True
    )

    service_areas = models.TextField(
        blank=True
    )

    competitors = models.TextField(
        blank=True
    )

    business_description = models.TextField(
        blank=True
    )


        # Hosting

    hosting_access = models.BooleanField(default=False)

    hosting_provider = models.CharField(
        max_length=255,
        blank=True
    )

    hosting_notes = models.TextField(
        blank=True
    )

    # Domain

    domain_access = models.BooleanField(default=False)

    domain_provider = models.CharField(
        max_length=255,
        blank=True
    )

    domain_notes = models.TextField(
        blank=True
    )

    # Google Analytics

    ga_access = models.BooleanField(default=False)

    ga_property_id = models.CharField(
        max_length=255,
        blank=True
    )

    ga_notes = models.TextField(
        blank=True
    )

    # Search Console

    gsc_access = models.BooleanField(default=False)

    gsc_property = models.CharField(
        max_length=255,
        blank=True
    )

    gsc_notes = models.TextField(
        blank=True
    )

    # Google Ads

    google_ads_access = models.BooleanField(default=False)

    google_ads_customer_id = models.CharField(
        max_length=255,
        blank=True
    )

    google_ads_notes = models.TextField(
        blank=True
    )

    # Meta

    meta_access = models.BooleanField(default=False)

    meta_business_id = models.CharField(
        max_length=255,
        blank=True
    )

    meta_notes = models.TextField(
        blank=True
    )

    # YouTube

    youtube_access = models.BooleanField(default=False)

    youtube_channel_name = models.CharField(
        max_length=255,
        blank=True
    )

    youtube_access_email = models.EmailField(
        blank=True
    )

    youtube_notes = models.TextField(
        blank=True
    )

    # Social Media

    social_media_access = models.BooleanField(default=False)

    facebook_page = models.CharField(
        max_length=255,
        blank=True
    )

    instagram_handle = models.CharField(
        max_length=255,
        blank=True
    )

    linkedin_page = models.CharField(
        max_length=255,
        blank=True
    )

    twitter_handle = models.CharField(
        max_length=255,
        blank=True
    )

    social_notes = models.TextField(
        blank=True
    )
    kpi_defined = models.BooleanField(
        default=False
    )

    reporting_setup = models.BooleanField(
        default=False
    )

    team_assigned = models.BooleanField(
        default=False
    )

    deliverables_defined = models.BooleanField(
        default=False
    )

    onboarding_completed = models.BooleanField(
        default=False
    )

    onboarding_completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.client.name} Onboarding"
        )