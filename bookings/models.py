from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from accounts.models import User
from services.models import Service

class Booking(models.Model):
    """Service bookings made by customers"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_bookings',
                                 limit_choices_to={'user_type': 'customer'})
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer_bookings',
                                   limit_choices_to={'user_type': 'freelancer'})
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    customer_notes = models.TextField(blank=True, help_text="Special instructions from customer")
    freelancer_notes = models.TextField(blank=True, help_text="Notes from freelancer")
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Booking #{self.id} - {self.service.title} by {self.customer.username}"
    
    def can_cancel(self):
        """Check if booking can be cancelled by customer"""
        if self.status not in ['pending', 'accepted']:
            return False
        
        booking_datetime = timezone.make_aware(
            timezone.datetime.combine(self.booking_date, self.booking_time)
        )
        time_difference = booking_datetime - timezone.now()
        cancellation_limit = timedelta(hours=settings.BOOKING_CANCELLATION_HOURS)
        
        return time_difference > cancellation_limit
    
    def cancel_booking(self):
        """Cancel the booking"""
        if self.can_cancel():
            self.status = 'cancelled'
            self.cancelled_at = timezone.now()
            self.save()
            return True
        return False
    
    def accept_booking(self):
        """Freelancer accepts the booking"""
        if self.status == 'pending':
            self.status = 'accepted'
            self.accepted_at = timezone.now()
            self.save()
            return True
        return False
    
    def reject_booking(self):
        """Freelancer rejects the booking"""
        if self.status == 'pending':
            self.status = 'rejected'
            self.save()
            return True
        return False
    
    def complete_booking(self):
        """Mark booking as completed"""
        if self.status == 'accepted':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()
            
            # Update freelancer stats
            profile = self.freelancer.freelancer_profile
            profile.completed_bookings += 1
            profile.save()
            
            return True
        return False
    
    class Meta:
        ordering = ['-created_at']


class BookingHistory(models.Model):
    """Track booking status changes"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='history')
    status = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking #{self.booking.id} - {self.status}"
    
    class Meta:
        verbose_name_plural = 'Booking Histories'
        ordering = ['-changed_at']
