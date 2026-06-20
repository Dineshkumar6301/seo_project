
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="activity",
            name="checklist_id_ref",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="activity",
            name="module_id_ref",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="activity",
            name="service_id_ref",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
