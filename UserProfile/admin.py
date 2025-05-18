from django.contrib import admin
from .models import Profile  # Adjust the import path based on your project structure

# Register your models here.
@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    pass