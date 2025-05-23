from django.contrib import admin

from payments.models import Payment


# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'amount', 'status', 'stripe_payment_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'project__title', 'payment_id')
    readonly_fields = ('created_at',)