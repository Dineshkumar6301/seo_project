
from django.db import models



class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name




class Project(models.Model):

    name = models.CharField(max_length=255)

    client = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        related_name='projects'
    )

    start_date = models.DateField()

    owner = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



class Service(models.Model):

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100,
        unique=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name




class ProjectService(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_services'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='service_projects'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'service')

    def __str__(self):
        return f"{self.project.name} - {self.service.name}"



class ServiceModule(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='modules'
    )

    name = models.CharField(max_length=200)

    order = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.service.name} - {self.name}"


class ChecklistTemplate(models.Model):

    module = models.ForeignKey(
        ServiceModule,
        on_delete=models.CASCADE,
        related_name='checklists'
    )

    item = models.CharField(max_length=255)

    order = models.IntegerField(default=0)

    recurring = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'item']

    def __str__(self):
        return self.item



class ProjectChecklist(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_checklists'
    )

    template = models.ForeignKey(
        ChecklistTemplate,
        on_delete=models.CASCADE,
        related_name='project_checklists'
    )

    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_project_checklists'
    )

    status = models.CharField(
        max_length=30,
        default='Pending'
    )

    notes = models.TextField(
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )



class TaskField(models.Model):

    FIELD_TYPES = [
        ('text', 'Text'),
        ('textarea', 'Textarea'),
        ('url', 'URL'),
        ('number', 'Number'),
        ('file', 'File'),
        ('select', 'Dropdown'),
        ('date', 'Date'),
    ]

    checklist_template = models.ForeignKey(
        ChecklistTemplate,
        on_delete=models.CASCADE,
        related_name='fields'
    )

    label = models.CharField(max_length=100)

    field_name = models.CharField(max_length=100)

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

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class ActivityLog(models.Model):

    project_checklist = models.ForeignKey(
        ProjectChecklist,
        on_delete=models.CASCADE,
        related_name='activities'
    )

    employee = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='project_activity_logs'
    )

    description = models.TextField()

    hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee} - {self.project_checklist}"



class ActivityFieldValue(models.Model):

    activity = models.ForeignKey(
        ActivityLog,
        on_delete=models.CASCADE,
        related_name='field_values'
    )

    field = models.ForeignKey(
        TaskField,
        on_delete=models.CASCADE
    )

    value = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.field.label}"
    


from django.db import models
from activities.models import Activity
from projects.models import Project


class KeywordRank(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )

    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    keyword = models.CharField(
        max_length=500
    )

    website = models.URLField()

    found = models.BooleanField(
        default=False
    )

    rank = models.IntegerField(
        null=True,
        blank=True
    )

    ranking_url = models.URLField(
        null=True,
        blank=True
    )

    checked_at = models.DateTimeField(
        auto_now_add=True
    )

    api_response = models.JSONField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.keyword} - {self.rank}"
    

class KeywordRankResult(models.Model):

    keyword_rank = models.ForeignKey(
        KeywordRank,
        on_delete=models.CASCADE,
        related_name="results"
    )

    serp_rank = models.IntegerField()

    result_type = models.CharField(
        max_length=50,
        blank=True
    )

    title = models.TextField(
        blank=True
    )

    domain = models.CharField(
        max_length=500,
        blank=True
    )

    url = models.URLField(
        max_length=1000,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    breadcrumb = models.TextField(
        blank=True
    )