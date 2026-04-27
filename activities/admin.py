from django.contrib import admin
from .models import Checklist, Activity


# ===============================
# CHECKLIST ADMIN
# ===============================
@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):

    list_display = (
        'project',
        'service',
        'item',
        'status',
        'order',
        'is_active',
        'completed_by',
        'created_at'
    )

    list_filter = (
        'project',
        'service',
        'status',
        'is_active',
        'created_at'
    )

    search_fields = (
        'item',
        'project__name',
        'service__name'
    )

    ordering = ('order',)

    list_editable = ('status', 'order', 'is_active')

    date_hierarchy = 'created_at'

from django.conf import settings
# ===============================
# ACTIVITY ADMIN
# ===============================
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'project',
        'service',
        'task_title',
        'date',
        'status',
        'created_at'
    )

    list_filter = (
        'project',
        'service',
        'status',
        'date',
        'created_at'
    )

    search_fields = (
        'task_title',
        'user__username',
        'project__name',
        'service__name'
    )

    ordering = ('-created_at',)

    date_hierarchy = 'date'

    list_editable = ('status',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'project', 'service', 'date')
        }),
        ('Task Details', {
            'fields': ('task_title', 'checklist_item')
        }),
        ('Work Info', {
            'fields': ('keyword', 'completed_work', 'proof_link', 'remarks')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Meta', {
            'fields': ('created_at',)
        }),
    )