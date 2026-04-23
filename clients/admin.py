from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'user',
        'website', 'industry', 'contact_email'
    )
    search_fields = (
        'name', 'user__email', 'contact_email', 'industry'
    )
    list_filter = ('industry',)
    ordering = ('-id',)

    autocomplete_fields = ('user',)

    fieldsets = (
        ("Basic Info", {
            'fields': ('user', 'name')
        }),
        ("Business Info", {
            'fields': ('website', 'industry')
        }),
        ("Contact Info", {
            'fields': ('contact_email',)
        }),
    )