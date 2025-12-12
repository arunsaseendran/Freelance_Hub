from django.urls import path
from . import views, admin_views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/freelancer/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    path('profile/', views.profile, name='profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('freelancers/', views.freelancer_list, name='freelancer_list'),
    path('freelancers/<int:pk>/', views.freelancer_detail, name='freelancer_detail'),
    
    # Admin Dashboard URLs
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin_dash'),
    path('admin/freelancers/', admin_views.freelancer_list, name='admin_freelancer_list'),
    path('admin/freelancers/<int:user_id>/', admin_views.freelancer_detail, name='admin_freelancer_detail'),
    path('admin/freelancers/<int:user_id>/approve/', admin_views.approve_freelancer, name='admin_approve_freelancer'),
    path('admin/freelancers/<int:user_id>/reject/', admin_views.reject_freelancer, name='admin_reject_freelancer'),
    path('admin/freelancers/<int:user_id>/delete/', admin_views.delete_freelancer, name='admin_delete_freelancer'),
    path('admin/freelancers/<int:user_id>/toggle-status/', admin_views.toggle_freelancer_status, name='admin_toggle_status'),
    
    # User Management URLs
    path('admin/users/', admin_views.user_list, name='admin_user_list'),
    path('admin/users/<int:user_id>/toggle-status/', admin_views.toggle_user_status, name='admin_toggle_user_status'),
    path('admin/users/<int:user_id>/delete/', admin_views.delete_user, name='admin_delete_user'),
    
    # Service Management URLs
    path('admin/services/', admin_views.service_list_admin, name='admin_service_list'),
    path('admin/services/<int:service_id>/approve/', admin_views.approve_service, name='admin_approve_service'),
    path('admin/services/<int:service_id>/reject/', admin_views.reject_service, name='admin_reject_service'),
    path('admin/services/<int:service_id>/delete/', admin_views.delete_service, name='admin_delete_service'),
    
    # Category Management URLs
    path('admin/categories/', admin_views.category_list_admin, name='admin_category_list'),
    path('admin/categories/add/', admin_views.add_category, name='admin_add_category'),
    path('admin/categories/<int:category_id>/edit/', admin_views.edit_category, name='admin_edit_category'),
    path('admin/categories/<int:category_id>/delete/', admin_views.delete_category, name='admin_delete_category'),
    path('admin/categories/<int:category_id>/toggle-status/', admin_views.toggle_category_status, name='admin_toggle_category_status'),
]
