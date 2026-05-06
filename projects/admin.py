from django.contrib import admin
from .models import (
    ServiceCategory,
    Project,
    Service,
    ProjectService,
    ChecklistTemplate,
    ServiceTask,
    TaskField
)


# =====================================================
# TASK FIELD INLINE
# =====================================================
class TaskFieldInline(admin.TabularInline):
    model = TaskField
    extra = 1


# =====================================================
# SERVICE TASK ADMIN
# =====================================================
@admin.register(ServiceTask)
class ServiceTaskAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'service',
        'name',
        'is_active',
        'order'
    )

    list_filter = (
        'service',
        'is_active'
    )

    search_fields = (
        'name',
        'service__name'
    )

    ordering = ('service', 'order')

    inlines = [TaskFieldInline]


# =====================================================
# SERVICE CATEGORY ADMIN
# =====================================================
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name'
    )

    search_fields = (
        'name',
    )


# =====================================================
# PROJECT SERVICE INLINE
# =====================================================
class ProjectServiceInline(admin.TabularInline):
    model = ProjectService
    extra = 1


# =====================================================
# PROJECT ADMIN
# =====================================================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'client',
        'owner',
        'start_date'
    )

    search_fields = (
        'name',
        'client__name'
    )

    list_filter = (
        'start_date',
    )

    inlines = [ProjectServiceInline]


# =====================================================
# SERVICE ADMIN
# =====================================================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'is_active'
    )

    list_filter = (
        'category',
        'is_active'
    )

    search_fields = (
        'name',
    )


# =====================================================
# PROJECT SERVICE ADMIN
# =====================================================
@admin.register(ProjectService)
class ProjectServiceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'project',
        'service'
    )

    list_filter = (
        'project',
        'service'
    )

    search_fields = (
        'project__name',
        'service__name'
    )


# =====================================================
# CHECKLIST TEMPLATE ADMIN
# =====================================================
@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'service',
        'item',
        'order',
        'is_active'
    )

    list_filter = (
        'service',
        'is_active'
    )

    search_fields = (
        'item',
        'service__name'
    )

    ordering = (
        'service',
        'order'
    )


# =====================================================
# TASK FIELD ADMIN
# =====================================================
@admin.register(TaskField)
class TaskFieldAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'task',
        'name',
        'label',
        'field_type',
        'required',
        'order'
    )

    list_filter = (
        'field_type',
        'required'
    )

    search_fields = (
        'name',
        'label',
        'task__name'
    )

    ordering = (
        'task',
        'order'
    )