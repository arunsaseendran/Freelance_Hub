from django.contrib import admin
from .models import Booking, BookingHistory

class BookingHistoryInline(admin.TabularInline):
    model = BookingHistory
    extra = 0
    readonly_fields = ['status', 'notes', 'changed_by', 'changed_at']
    can_delete = False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'freelancer', 'service', 'booking_date', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'booking_date', 'created_at']
    search_fields = ['customer__username', 'freelancer__username', 'service__title']
    readonly_fields = ['created_at', 'updated_at', 'accepted_at', 'completed_at', 'cancelled_at']
    inlines = [BookingHistoryInline]


@admin.register(BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ['booking', 'status', 'changed_by', 'changed_at']
    list_filter = ['status', 'changed_at']
    search_fields = ['booking__id', 'notes']
