from django.contrib import admin
from .models import Donation

# Register your models here.
@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'amount', 'payment_status', 'payment_id', 'created_at')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('user__username', 'project__title', 'payment_id')
    readonly_fields = ('created_at',)
