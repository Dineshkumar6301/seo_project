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


class Activity(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='activities' 
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE
    )
    checklist_item = models.ForeignKey(
        Checklist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date = models.DateField()

    task_title = models.CharField(max_length=255)

    planned_work = models.TextField(blank=True)
    completed_work = models.TextField(blank=True)

    proof_link = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_activities"
    )

    approved_at = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

        unique_together = ['user', 'project', 'service', 'date', 'task_title']

    def __str__(self):
        return f"{self.user} | {self.project} | {self.service} | {self.date}"