from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    ProjectService,
    ChecklistTemplate
)

from activities.models import Checklist


@receiver(post_save, sender=ProjectService)
def create_project_checklists(
    sender,
    instance,
    created,
    **kwargs
):

    if not created:
        return

    service = instance.service
    project = instance.project

    templates = ChecklistTemplate.objects.filter(
        service=service,
        is_active=True
    )

    for template in templates:

        Checklist.objects.get_or_create(

            project=project,

            service=service,

            item=template.item,

            defaults={
                "order": template.order,
                "status": "pending"
            }
        )