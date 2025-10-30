from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, AllValuesFieldListFilter

from .models import Status

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ['name', 'body']
    list_filter = (
        ('name', AllValuesFieldListFilter),
        ('created_at', DateFieldListFilter),
    )

