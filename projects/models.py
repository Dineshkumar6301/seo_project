from django.db import models


# ==========================================
# SERVICE CATEGORY
# ==========================================
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ==========================================
# PROJECT
# ==========================================
class Project(models.Model):
    name = models.CharField(max_length=255)

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE
    )

    start_date = models.DateField()

    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


# ==========================================
# GLOBAL SERVICES
# ==========================================
class Service(models.Model):

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name="services",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100, unique=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# ==========================================
# PROJECT ↔ SERVICES
# ==========================================
class ProjectService(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_services"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="service_projects"
    )

    class Meta:
        unique_together = ('project', 'service')

    def __str__(self):
        return f"{self.project.name} - {self.service.name}"


# ==========================================
# CHECKLIST TEMPLATE
# ==========================================
class ChecklistTemplate(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="checklist_templates"
    )

    item = models.CharField(max_length=255)

    order = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service.name} - {self.item}"


# ==========================================
# SERVICE TASKS
# ==========================================
class ServiceTask(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.service.name} - {self.name}"


# ==========================================
# TASK FIELDS
# ==========================================
class TaskField(models.Model):

    FIELD_TYPES = [
        ('text', 'Text'),
        ('url', 'URL'),
        ('number', 'Number'),
        ('file', 'File'),
        ('textarea', 'Textarea'),
        ('select', 'Dropdown'),
    ]

    task = models.ForeignKey(
        ServiceTask,
        on_delete=models.CASCADE,
        related_name="fields"
    )

    name = models.CharField(max_length=100)

    label = models.CharField(max_length=100)

    field_type = models.CharField(
        max_length=50,
        choices=FIELD_TYPES
    )

    required = models.BooleanField(default=False)

    order = models.IntegerField(default=0)

    options = models.JSONField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.task.name} - {self.name}"