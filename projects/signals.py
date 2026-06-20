from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    ProjectService,
    ChecklistTemplate,
    ProjectChecklist,
)


@receiver(post_save, sender=ProjectService)
def create_project_checklists(
    sender,
    instance,
    created,
    **kwargs
):

    if kwargs.get("raw", False):
        return

    if not created:
        return

    project = instance.project
    service = instance.service

    templates = ChecklistTemplate.objects.filter(
        module__service=service,
        is_active=True
    )

    for template in templates:

        ProjectChecklist.objects.get_or_create(
            project=project,
            template=template,
            defaults={
                "status": "Approved"
            }
        )