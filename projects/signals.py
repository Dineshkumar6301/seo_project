from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Project,ChecklistTemplate




@receiver(m2m_changed, sender=Project.services.through)
def create_checklist_on_service_add(sender, instance, action, pk_set, **kwargs):

    # Only trigger when services are added
    if action == 'post_add':

        for service_id in pk_set:

            templates = ChecklistTemplate.objects.filter(
                service_id=service_id,
                is_active=True
            )

            for template in templates:

                # 🔒 Prevent duplicates
                exists = ChecklistTemplate.objects.filter(
                    project=instance,
                    service_id=service_id,
                    item=template.title
                ).exists()

                if not exists:
                    ChecklistTemplate.objects.create(
                        project=instance,
                        service_id=service_id,
                        item=template.title,
                        order=template.order,
                        status='pending'
                    )