from django.contrib import admin
from .models import Report

# Register your models here.
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reason', 'user', 'project', 'comment', 'replay', 'is_resolved', 'created_at', 'updated_at')
    list_filter = ('is_resolved', 'created_at', 'updated_at')
    search_fields = ('reason', 'user__username', 'project__title')
    readonly_fields = ('created_at', 'updated_at')
