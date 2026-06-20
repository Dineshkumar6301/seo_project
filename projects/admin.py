from django.contrib import admin
from .models import (
    Project,
    ServiceCategory,
    Service,
    ServiceModule,
    ChecklistTemplate,
    ProjectChecklist,
    TaskField,

)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )

from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "is_active",
    )

    list_filter = (
        "category",
        "is_active",
    )

    search_fields = (
        "name",
        "category__name",
    )

    list_editable = (
        "is_active",
    )

    ordering = (
        "category",
        "name",
    )

    list_per_page = 50

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )


from django.contrib import admin

from .models import ServiceModule


@admin.register(ServiceModule)
class ServiceModuleAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "service",
        "order",
        "is_active",
    )

    list_filter = (
        "service",
        "is_active",
    )

    search_fields = (
        "name",
        "service__name",
    )

    list_editable = (
        "order",
        "is_active",
    )

    ordering = (
        "service",
        "order",
        "name",
    )

    list_per_page = 50

from django.contrib import admin

from .models import ChecklistTemplate


@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "item",
        "module",
        "order",
        "recurring",
        "is_active",
    )

    list_filter = (
        "module",
        "recurring",
        "is_active",
    )

    search_fields = (
        "item",
        "module__name",
    )

    ordering = (
        "module",
        "order",
        "item",
    )

    list_editable = (
        "order",
        "recurring",
        "is_active",
    )

    list_per_page = 50


from django.contrib import admin

from .models import ProjectChecklist


@admin.register(ProjectChecklist)
class ProjectChecklistAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "project",
        "template",
        "assigned_to",
        "status",
        "completed_at",
    )

    list_filter = (
        "status",
        "project",
        "assigned_to",
    )

    search_fields = (
        "project__name",
        "template__item",
        "assigned_to__email",
        "notes",
    )

    readonly_fields = (
        "completed_at",
    )

    list_per_page = 50

@admin.register(TaskField)

class TaskFieldAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "checklist_template",
        "label",
        "field_name",
        "field_type",
        "required",
        "order"
    )

    list_filter = (
        "field_type",
        "required",
    )

    search_fields = (
        "label",
        "field_name",
        "checklist_template__item"
    )

    ordering = (
        "checklist_template",
        "order"
    )


from django.contrib import admin
from .models import KeywordRank, KeywordRankResult


@admin.register(KeywordRank)
class KeywordRankAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "project",
        "keyword",
        "website",
        "rank",
        "found",
        "checked_at",
    )

    search_fields = (
        "keyword",
        "website",
        "project__name",
    )

    list_filter = (
        "found",
        "checked_at",
    )

    readonly_fields = (
        "checked_at",
        "api_response",
    )


@admin.register(KeywordRankResult)
class KeywordRankResultAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "keyword_rank",
        "serp_rank",
        "result_type",
        "domain",
    )

    search_fields = (
        "domain",
        "title",
        "url",
    )

    list_filter = (
        "result_type",
    )