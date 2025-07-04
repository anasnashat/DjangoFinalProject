from django.contrib import admin
from projects.models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'category', 'total_target', 'starting_date', 'ending_date', 'is_active', 'is_featured')
    list_filter = ('is_active', 'is_featured', 'category', 'starting_date', 'ending_date')
    search_fields = ('title', 'details', 'created_by__username', 'category__name')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tags',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    