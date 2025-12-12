from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, FreelancerProfile, CustomerProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile based on user type"""
    if created:
        if instance.user_type == 'freelancer':
            FreelancerProfile.objects.create(user=instance)
        elif instance.user_type == 'customer':
            CustomerProfile.objects.create(user=instance)
