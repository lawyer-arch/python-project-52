from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, RelatedOnlyFieldListFilter

from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'author',
        'executor',
        'status',
        'created_at',
    )
    search_fields = ['name', 'body']
    list_filter = (
        ('created_at', DateFieldListFilter),
        ('executor', RelatedOnlyFieldListFilter),
        ('author', RelatedOnlyFieldListFilter),
    )
