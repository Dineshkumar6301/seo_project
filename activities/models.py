from django.db import models
from django.conf import settings
from projects.models import Project, Service


class Checklist(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='checklists'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )

    item = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    order = models.IntegerField(default=0)

    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.project.name} - {self.service.name} - {self.item}"



from django.db import models
from django.conf import settings


class Activity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    service = models.ForeignKey("projects.Service", on_delete=models.CASCADE)
    task_title = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    completed_work = models.TextField(blank=True, null=True)
    proof_link = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=20, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def get_proof_links(self):
        if not self.proof_link:
            return []
        return [link.strip() for link in self.proof_link.splitlines() if link.strip()]