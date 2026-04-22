from django.contrib import admin

from projects.models import Project
from django.contrib import admin
from .models import Service, ChecklistTemplate
# Register your models here.
admin.site.register(Project)


admin.site.register(Service)
admin.site.register(ChecklistTemplate)

