from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('id', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name', 'mobile')
    ordering = ('-id',)

    readonly_fields = ('last_login',)

    fieldsets = (
        ("Login Info", {
            'fields': ('email', 'password')
        }),
        ("Personal Info", {
            'fields': ('first_name', 'last_name', 'mobile')
        }),
        ("Permissions", {
            'fields': ('role', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ("Important Dates", {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        ("Create User", {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'designation', 'department')
    search_fields = ('user__email', 'designation', 'department', 'skills')
    list_filter = ('department', 'designation')
    autocomplete_fields = ('user',)

    fieldsets = (
        ("User Info", {
            'fields': ('user', 'phone', 'photo')
        }),
        ("Professional Info", {
            'fields': (
                'designation', 'department',
                'experience', 'skills'
            )
        }),
        ("Company Info", {
            'fields': (
                'company_name', 'website', 'industry'
            )
        }),
        ("Other Info", {
            'fields': ('location', 'bio')
        }),
    )

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Profile,
    PasswordResetToken,
    PasswordResetRequestLog
)



@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'token',
        'created_at',
        'is_expired'
    )

    search_fields = (
        'email',
        'token'
    )

    readonly_fields = (
        'created_at',
    )

    list_filter = (
        'created_at',
    )


@admin.register(PasswordResetRequestLog)
class PasswordResetRequestLogAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'created_at'
    )

    search_fields = (
        'email',
    )

    readonly_fields = (
        'created_at',
    )

    list_filter = (
        'created_at',
    )