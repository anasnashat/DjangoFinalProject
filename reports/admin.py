
from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_reason_display', 'user', 'get_reported_item', 'is_resolved', 'created_at','description')
    list_filter = ('is_resolved', 'reason', 'created_at')
    search_fields = ('description', 'user__username', 'project__title', 'comment__content')
    list_editable = ('is_resolved',)
    readonly_fields = ('created_at', 'updated_at')

    def get_reported_item(self, obj):
        if obj.project:
            return f"Project: {obj.project.title}"
        elif obj.comment:
            return f"Comment: {obj.comment.content[:50]}"
        return "Unknown"
    get_reported_item.short_description = 'Reported Item'