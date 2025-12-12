from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FreelancerProfile, CustomerProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_verified', 'created_at']
    list_filter = ['user_type', 'is_verified', 'is_active']
    search_fields = ['username', 'email', 'phone', 'city']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone', 'address', 'city', 'area', 'pincode', 
                      'profile_picture', 'is_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('user_type', 'phone', 'email')
        }),
    )


@admin.register(FreelancerProfile)
class FreelancerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'experience_years', 'payment_mode', 'rating', 'is_available']
    list_filter = ['payment_mode', 'is_available']
    search_fields = ['user__username', 'user__email', 'skills']


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_bookings']
    search_fields = ['user__username', 'user__email']
