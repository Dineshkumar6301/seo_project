from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0003_clientonboarding_business_description_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="clientonboarding",
            name="tag_manager_access",
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="domain_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="domain_provider",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="facebook_page",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="ga_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="ga_property_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="google_ads_customer_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="google_ads_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="gsc_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="gsc_property",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="hosting_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="hosting_provider",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="instagram_handle",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="linkedin_page",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="meta_business_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="meta_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="social_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="twitter_handle",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="youtube_access_email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="youtube_channel_name",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="clientonboarding",
            name="youtube_notes",
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name="clientonboarding",
            name="ga_access",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="clientonboarding",
            name="gsc_access",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="clientonboarding",
            name="meta_access",
            field=models.BooleanField(default=False),
        ),
    ]
