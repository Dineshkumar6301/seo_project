from django.contrib import admin
from .models import Activity, Checklist


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'project',
        'service_name',
        'task_type',
        'status',
        'date',
        'rank_checked',
        'last_rank',
        'rank_checked_at'
    )

    search_fields = (
        'project__name',
        'user__email',
        'service_name',
        'task_type',
    )

    list_filter = (
        'status',
        'date',
    )

    autocomplete_fields = (
        'project',
        'user',
    )

    ordering = (
        '-date',
        '-created_at',
    )


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'project',
        'service',
        'item',
        'status',
    )

    search_fields = (
        'project__name',
        'service__name',
        'item',
    )

    list_filter = (
        'status',
    )

    autocomplete_fields = (
        'project',
        'service',
    )

    ordering = (
        'order',
    )