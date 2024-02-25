from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile


class Admin(UserAdmin):
    list_display = ['phone', 'fullName', 'role', 'is_active']
    filter_horizontal = []
    list_filter = ['role', 'is_active']
    fieldsets = []
    ordering = ['last_name']


class PAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']


admin.site.register(User, Admin)

admin.site.register(Profile, PAdmin)
