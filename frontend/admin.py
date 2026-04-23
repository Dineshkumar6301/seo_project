from django.contrib import admin
from django.contrib import admin
from .models import ProjectServiceAssignment


@admin.register(ProjectServiceAssignment)
class ProjectServiceAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'project', 'service', 'user',
        'assigned_by', 'created_at'
    )
    search_fields = (
        'project__name',
        'service__name',
        'user__email',
        'assigned_by__email'
    )
    list_filter = ('project', 'service', 'created_at')
    ordering = ('-created_at',)

   
    readonly_fields = ('created_at',)

    fieldsets = (
        ("Assignment Info", {
            'fields': ('project', 'service', 'user')
        }),
        ("Tracking Info", {
            'fields': ('assigned_by', 'created_at')
        }),
    )