import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="address",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="client",
            name="contact_person",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="client",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.CreateModel(
            name="ClientOnboarding",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("website", models.URLField(blank=True)),
                ("competitors", models.TextField(blank=True)),
                ("target_audience", models.TextField(blank=True)),
                ("ga_access", models.BooleanField(default=False)),
                ("gsc_access", models.BooleanField(default=False)),
                ("tag_manager_access", models.BooleanField(default=False)),
                ("google_ads_access", models.BooleanField(default=False)),
                ("meta_access", models.BooleanField(default=False)),
                ("hosting_access", models.BooleanField(default=False)),
                ("domain_access", models.BooleanField(default=False)),
                ("onboarding_completed", models.BooleanField(default=False)),
                ("business_category", models.CharField(blank=True, max_length=255)),
                ("service_areas", models.TextField(blank=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "client",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="clients.client"
                    ),
                ),
            ],
        ),
    ]
