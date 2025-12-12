from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import random
import string

class User(AbstractUser):
    """Custom User model with role-based access"""
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('freelancer', 'Freelancer'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    class Meta:
        ordering = ['-created_at']


class FreelancerProfile(models.Model):
    """Extended profile for freelancers"""
    PAYMENT_MODE_CHOICES = (
        ('cash', 'Cash'),
        ('gpay', 'GPay'),
        ('both', 'Both'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    skills = models.TextField(help_text="Comma-separated skills")
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODE_CHOICES, default='both')
    gpay_number = models.CharField(max_length=15, blank=True, help_text="GPay mobile number")
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    total_bookings = models.IntegerField(default=0)
    completed_bookings = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Freelancer"
    
    def update_rating(self):
        """Update average rating from reviews"""
        from reviews.models import Review
        reviews = Review.objects.filter(freelancer=self.user, is_active=True)
        if reviews.exists():
            self.rating = reviews.aggregate(models.Avg('rating'))['rating__avg']
            self.total_reviews = reviews.count()
            self.save()


class CustomerProfile(models.Model):
    """Customer profile with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    total_bookings = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Customer"


class EmailOTP(models.Model):
    """Model to store email OTP for verification"""
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP for {self.email}"
    
    @classmethod
    def generate_otp(cls, email):
        """Generate a new OTP for the given email"""
        # Delete any existing unverified OTPs for this email
        cls.objects.filter(email=email, is_verified=False).delete()
        
        # Generate 6-digit OTP
        otp = ''.join(random.choices(string.digits, k=6))
        
        # Create new OTP record
        otp_record = cls.objects.create(email=email, otp=otp)
        return otp_record
    
    def is_expired(self):
        """Check if OTP is expired (10 minutes)"""
        from django.conf import settings
        expiry_time = self.created_at + timezone.timedelta(minutes=getattr(settings, 'OTP_EXPIRY_MINUTES', 10))
        return timezone.now() > expiry_time
    
    def verify(self, entered_otp):
        """Verify the entered OTP"""
        if self.is_expired():
            return False, "OTP has expired"
        
        if self.otp != entered_otp:
            return False, "Invalid OTP"
        
        self.is_verified = True
        self.save()
        return True, "OTP verified successfully"
