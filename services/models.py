from django.db import models
from accounts.models import User

class Category(models.Model):
    """Service categories like Cleaning, Electrical, Beauty, etc."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class SubCategory(models.Model):
    """Subcategories under main categories"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    class Meta:
        verbose_name_plural = 'SubCategories'
        ordering = ['category', 'name']
        unique_together = ['category', 'name']


class Service(models.Model):
    """Services offered by freelancers"""
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services', 
                                   limit_choices_to={'user_type': 'freelancer'})
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in INR")
    duration = models.IntegerField(help_text="Estimated duration in minutes")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approval required")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.freelancer.get_full_name()}"
    
    class Meta:
        ordering = ['-created_at']


class ServiceImage(models.Model):
    """Additional images for services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='service_images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.service.title}"
