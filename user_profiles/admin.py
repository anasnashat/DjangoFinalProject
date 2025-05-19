from django.contrib import admin
from .models import Profile  # Adjust the import path based on your projects structure

# Register your models here.
@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'country', 'phone_number', 'birthdate')
    list_filter = ('gender', 'country')
    search_fields = ('user__username', 'user__email', 'country', 'phone_number')
    raw_id_fields = ('user',)
