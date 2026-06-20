import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0002_client_address_client_contact_person_client_phone_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="clientonboarding",
            name="business_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="business_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="deliverables_defined",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="kpi_defined",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="onboarding_completed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="reporting_setup",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="social_media_access",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="team_assigned",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="youtube_access",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="clientonboarding",
            name="client",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="onboarding",
                to="clients.client",
            ),
        ),
        migrations.AlterField(
            model_name="clientonboarding",
            name="ga_access",
            field=models.BooleanField(
                default=False, verbose_name="Google Analytics Access"
            ),
        ),
        migrations.AlterField(
            model_name="clientonboarding",
            name="gsc_access",
            field=models.BooleanField(
                default=False, verbose_name="Google Search Console Access"
            ),
        ),
        migrations.AlterField(
            model_name="clientonboarding",
            name="meta_access",
            field=models.BooleanField(
                default=False, verbose_name="Meta Business Manager Access"
            ),
        ),
    ]
