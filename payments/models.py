from django.db import models
from django.utils import timezone
from accounts.models import User
from bookings.models import Booking

class Payment(models.Model):
    """Payment records for bookings"""
    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('gpay', 'GPay'),
        ('razorpay', 'Razorpay'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    transaction_id = models.CharField(max_length=100, blank=True, help_text="Payment gateway transaction ID")
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_details = models.TextField(blank=True, help_text="JSON data for payment gateway details")
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment #{self.id} - Booking #{self.booking.id} - {self.get_payment_method_display()}"
    
    def mark_completed(self, transaction_id=None):
        """Mark payment as completed"""
        self.status = 'completed'
        self.payment_date = timezone.now()
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()
    
    def mark_failed(self, reason=""):
        """Mark payment as failed"""
        self.status = 'failed'
        self.notes = reason
        self.save()
    
    class Meta:
        ordering = ['-created_at']


class Refund(models.Model):
    """Refund requests and processing"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    )
    
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='refund')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='refunds')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refund_requests')
    requested_at = models.DateTimeField(auto_now_add=True)
    
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='processed_refunds')
    processed_at = models.DateTimeField(null=True, blank=True)
    
    admin_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Refund #{self.id} - Payment #{self.payment.id}"
    
    def approve_refund(self, admin_user, notes=""):
        """Approve refund request"""
        self.status = 'approved'
        self.processed_by = admin_user
        self.processed_at = timezone.now()
        self.admin_notes = notes
        self.save()
    
    def reject_refund(self, admin_user, notes=""):
        """Reject refund request"""
        self.status = 'rejected'
        self.processed_by = admin_user
        self.processed_at = timezone.now()
        self.admin_notes = notes
        self.save()
    
    def process_refund(self):
        """Mark refund as processed"""
        if self.status == 'approved':
            self.status = 'processed'
            self.payment.status = 'refunded'
            self.payment.save()
            self.save()
            return True
        return False
    
    class Meta:
        ordering = ['-requested_at']


class Transaction(models.Model):
    """Transaction history for all financial activities"""
    TRANSACTION_TYPE_CHOICES = (
        ('payment', 'Payment'),
        ('refund', 'Refund'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='transactions')
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - ₹{self.amount} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
