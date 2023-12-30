from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register()
class CAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']
