from django.contrib import admin
from .models import Reply

# Register your models here.
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('replay', 'user', 'comment', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('replay', 'user__username', 'comment__content')
    readonly_fields = ('created_at', 'updated_at')
