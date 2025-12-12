from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Booking, BookingHistory

@receiver(post_save, sender=Booking)
def create_booking_history(sender, instance, created, **kwargs):
    """Create history entry when booking is created or updated"""
    if created:
        BookingHistory.objects.create(
            booking=instance,
            status=instance.status,
            notes="Booking created",
            changed_by=instance.customer
        )


@receiver(pre_save, sender=Booking)
def track_status_change(sender, instance, **kwargs):
    """Track status changes in booking"""
    if instance.pk:
        try:
            old_instance = Booking.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                # Will be saved after the booking is saved
                instance._status_changed = True
                instance._old_status = old_instance.status
        except Booking.DoesNotExist:
            pass


@receiver(post_save, sender=Booking)
def save_status_change_history(sender, instance, created, **kwargs):
    """Save status change to history"""
    if not created and hasattr(instance, '_status_changed'):
        BookingHistory.objects.create(
            booking=instance,
            status=instance.status,
            notes=f"Status changed from {instance._old_status} to {instance.status}",
            changed_by=None  # Can be enhanced to track who made the change
        )
