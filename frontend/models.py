from django.db import models
from accounts.models import User
from projects.models import Project, Service



class ProjectServiceAssignment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_by_admin'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'user', 'service']