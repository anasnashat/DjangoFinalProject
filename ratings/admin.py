from django.contrib import admin
from .models import Rating

# Register your models here.
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'project__title')
    readonly_fields = ('created_at', 'updated_at')
