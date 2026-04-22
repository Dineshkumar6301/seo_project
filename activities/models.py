from django.db import models
from django.conf import settings
from projects.models import Project, Service


# ==========================================
# CHECKLIST MODEL (Planned Work / Template)
# ==========================================
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


# ==========================================
# ACTIVITY MODEL (Daily Work)
# ==========================================
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
        related_name='activities'   # 🔥 ADD THIS
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

    # 🔥 Link to checklist (optional but powerful)
    checklist_item = models.ForeignKey(
        Checklist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # 🔥 Critical for date-based UI
    date = models.DateField()

    task_title = models.CharField(max_length=255)

    planned_work = models.TextField(blank=True)
    completed_work = models.TextField(blank=True)

    proof_link = models.URLField(blank=True)
    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

        # 🔥 Prevent duplicate same-day entries
        unique_together = ['user', 'project', 'service', 'date', 'task_title']

    def __str__(self):
        return f"{self.user} | {self.project} | {self.service} | {self.date}"