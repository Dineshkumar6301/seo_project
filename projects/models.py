from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE)

    services = models.ManyToManyField(Service, blank=True)

    start_date = models.DateField()
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ChecklistTemplate(models.Model):
  
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='template_checklists'
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='pending')
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.item