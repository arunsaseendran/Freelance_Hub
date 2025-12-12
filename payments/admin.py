from django.contrib import admin
from .models import Payment, Refund, Transaction

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'customer', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['booking__id', 'customer__username', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'amount', 'status', 'requested_by', 'requested_at', 'processed_by']
    list_filter = ['status', 'requested_at']
    search_fields = ['payment__id', 'booking__id', 'requested_by__username']
    readonly_fields = ['requested_at', 'processed_at']
    
    actions = ['approve_refunds', 'reject_refunds']
    
    def approve_refunds(self, request, queryset):
        for refund in queryset.filter(status='pending'):
            refund.approve_refund(request.user, "Approved by admin")
        self.message_user(request, f"{queryset.count()} refunds approved.")
    approve_refunds.short_description = "Approve selected refunds"
    
    def reject_refunds(self, request, queryset):
        for refund in queryset.filter(status='pending'):
            refund.reject_refund(request.user, "Rejected by admin")
        self.message_user(request, f"{queryset.count()} refunds rejected.")
    reject_refunds.short_description = "Reject selected refunds"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'booking', 'transaction_type', 'amount', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['user__username', 'booking__id', 'description']
