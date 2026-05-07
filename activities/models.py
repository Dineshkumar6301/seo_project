from django.db import models
from django.conf import settings
from projects.models import Project, Service

# =========================================================
# ACTIVITY
# =========================================================
class Activity(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # ==========================================
    # BASIC INFO
    # ==========================================
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

    date = models.DateField()

    # ==========================================
    # DYNAMIC STRUCTURE
    # ==========================================
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    service_name = models.CharField(
        max_length=100
    )

    task_type = models.CharField(
        max_length=100
    )

    # ==========================================
    # DYNAMIC FORM DATA
    # ==========================================
    dynamic_data = models.JSONField(
        default=dict,
        blank=True
    )

    # ==========================================
    # STATUS
    # ==========================================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # ==========================================
    # TIMESTAMPS
    # ==========================================
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ==========================================
    # META
    # ==========================================
    class Meta:

        ordering = ['-date', '-created_at']

        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['project']),
            models.Index(fields=['service_name']),
            models.Index(fields=['task_type']),
            models.Index(fields=['status']),
        ]

    # ==========================================
    # STRING
    # ==========================================
    def __str__(self):

        return (
            f"{self.project.name} | "
            f"{self.service_name} | "
            f"{self.task_type}"
        )


# =========================================================
# CHECKLIST
# =========================================================
class Checklist(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='checklists'
    )

    service = models.ForeignKey(
        'projects.Service',
        on_delete=models.CASCADE,
        related_name='checklists'
    )

    item = models.CharField(
        max_length=255
    )

    order = models.IntegerField(
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ['order', 'id']

    def __str__(self):

        return (
            f"{self.project.name} - "
            f"{self.service.name} - "
            f"{self.item}"
        )