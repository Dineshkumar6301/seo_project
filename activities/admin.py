from django.contrib import admin
from .models import Activity, Checklist


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'project',
        'category',
        'service_name',
        'task_type',
        'status',
        'date',
        'created_at'
    )

    list_filter = (
        'category',
        'service_name',
        'task_type',
        'status',
        'date'
    )

    search_fields = (
        'user__first_name',
        'user__last_name',
        'project__name',
        'service_name',
        'task_type'
    )

    readonly_fields = (
        'created_at',
        'updated_at'
    )

    ordering = (
        '-date',
        '-created_at'
    )

    list_per_page = 50

    fieldsets = (

        ("Basic Information", {
            "fields": (
                'user',
                'project',
                'date'
            )
        }),

        ("Dynamic Structure", {
            "fields": (
                'category',
                'service_name',
                'task_type'
            )
        }),

        ("Dynamic Form Data", {
            "fields": (
                'dynamic_data',
            )
        }),

        ("Status", {
            "fields": (
                'status',
            )
        }),

        ("Timestamps", {
            "fields": (
                'created_at',
                'updated_at'
            )
        }),
    )

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'project',
        'service',
        'item',
        'status',
        'order',
        'completed_by',
        'created_at'
    )

    list_filter = (
        'status',
        'service',
        'project'
    )

    search_fields = (
        'project__name',
        'service__name',
        'item'
    )

    ordering = (
        'order',
        'id'
    )

    list_per_page = 50

    readonly_fields = (
        'created_at',
        'completed_at'
    )

    fieldsets = (

        ("Checklist Information", {
            "fields": (
                'project',
                'service',
                'item',
                'order'
            )
        }),

        ("Status", {
            "fields": (
                'status',
                'completed_by',
                'completed_at'
            )
        }),

        ("Created", {
            "fields": (
                'created_at',
            )
        }),
    )