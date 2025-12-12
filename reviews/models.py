from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from bookings.models import Booking

class Review(models.Model):
    """Customer reviews and ratings for freelancers"""
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given',
                                 limit_choices_to={'user_type': 'customer'})
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received',
                                   limit_choices_to={'user_type': 'freelancer'})
    
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review by {self.customer.username} for {self.freelancer.username} - {self.rating}★"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update freelancer rating
        self.freelancer.freelancer_profile.update_rating()
    
    class Meta:
        ordering = ['-created_at']


class ReviewResponse(models.Model):
    """Freelancer responses to reviews"""
    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='response')
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_responses')
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to review #{self.review.id}"
    
    class Meta:
        ordering = ['-created_at']


class Report(models.Model):
    """Reports for inappropriate reviews or content"""
    REPORT_TYPE_CHOICES = (
        ('review', 'Review'),
        ('user', 'User'),
        ('service', 'Service'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    )
    
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    
    # Generic fields for different report types
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='reports')
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='reports_received')
    
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    admin_notes = models.TextField(blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='reports_resolved')
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report #{self.id} - {self.get_report_type_display()} by {self.reported_by.username}"
    
    class Meta:
        ordering = ['-created_at']
