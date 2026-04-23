from django.contrib import admin
from .models import Service, Project, ChecklistTemplate


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'client', 'owner', 'start_date')
    search_fields = ('name', 'client__name', 'owner__email')
    list_filter = ('start_date', 'client')
    ordering = ('-id',)

    autocomplete_fields = ('client', 'owner')
    filter_horizontal = ('services',)

    fieldsets = (
        ("Basic Info", {
            'fields': ('name', 'client', 'owner')
        }),
        ("Project Details", {
            'fields': ('services', 'start_date')
        }),
    )


@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'service', 'item', 'status', 'is_active')
    search_fields = ('item', 'project__name', 'service__name')
    list_filter = ('status', 'is_active', 'project', 'service')
    ordering = ('id',)

    autocomplete_fields = ('project', 'service')

    fieldsets = (
        ("Checklist Info", {
            'fields': ('project', 'service', 'item')
        }),
        ("Status Info", {
            'fields': ('status', 'is_active')
        }),
    )