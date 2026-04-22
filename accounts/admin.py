from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active')
    search_fields = ('email','role')
    list_filter = ('role', 'is_active')

admin.site.register(User, UserAdmin)