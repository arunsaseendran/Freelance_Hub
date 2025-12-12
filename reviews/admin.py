from django.contrib import admin
from .models import Review, ReviewResponse, Report

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'freelancer', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['customer__username', 'freelancer__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ReviewResponse)
class ReviewResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'review', 'freelancer', 'created_at']
    search_fields = ['freelancer__username', 'response_text']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'report_type', 'reported_by', 'status', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['reported_by__username', 'reason']
    readonly_fields = ['created_at', 'resolved_at']
