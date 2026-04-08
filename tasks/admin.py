from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'created_by', 'assigned_to', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
    raw_id_fields = ('created_by', 'assigned_to')
