"""
Admin configuration for tasks.
"""

from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "course", "due_date", "completed", "created_at"]
    list_filter = ["completed", "due_date", "user"]
    search_fields = ["title", "description", "course"]
    date_hierarchy = "due_date"
    readonly_fields = ["created_at"]
