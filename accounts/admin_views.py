from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from .models import User, FreelancerProfile
from services.models import Service, Category, SubCategory
from bookings.models import Booking


def admin_required(view_func):
    """Decorator to check if user is admin"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access admin dashboard.')
            return redirect('accounts:login')
        if request.user.user_type != 'admin' and not request.user.is_superuser:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    """Main admin dashboard"""
    # Get statistics
    total_users = User.objects.count()
    total_freelancers = User.objects.filter(user_type='freelancer').count()
    pending_freelancers = User.objects.filter(user_type='freelancer', is_verified=False).count()
    active_freelancers = User.objects.filter(user_type='freelancer', is_verified=True).count()
    total_customers = User.objects.filter(user_type='customer').count()
    total_services = Service.objects.count()
    pending_services = Service.objects.filter(is_approved=False).count()
    approved_services = Service.objects.filter(is_approved=True).count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    # Recent customers only
    recent_users = User.objects.filter(user_type='customer').order_by('-created_at')[:5]
    
    # Recent freelancers
    recent_freelancers = User.objects.filter(user_type='freelancer').order_by('-created_at')[:5]
    
    # Top rated freelancers
    top_freelancers = User.objects.filter(
        user_type='freelancer',
        is_verified=True
    ).select_related('freelancer_profile').order_by('-freelancer_profile__rating')[:5]
    
    # Recent customers
    recent_customers = User.objects.filter(user_type='customer').order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_freelancers': total_freelancers,
        'pending_freelancers': pending_freelancers,
        'active_freelancers': active_freelancers,
        'total_customers': total_customers,
        'total_services': total_services,
        'pending_services': pending_services,
        'approved_services': approved_services,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'recent_users': recent_users,
        'recent_freelancers': recent_freelancers,
        'top_freelancers': top_freelancers,
        'recent_customers': recent_customers,
    }
    
    return render(request, 'admin/dashboard.html', context)


@admin_required
def freelancer_list(request):
    """List all freelancers with filters"""
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    freelancers = User.objects.filter(user_type='freelancer').select_related('freelancer_profile')
    
    # Apply filters
    if status_filter == 'pending':
        freelancers = freelancers.filter(is_verified=False)
    elif status_filter == 'approved':
        freelancers = freelancers.filter(is_verified=True)
    
    # Apply search
    if search_query:
        freelancers = freelancers.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    freelancers = freelancers.order_by('-created_at')
    
    context = {
        'freelancers': freelancers,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'admin/freelancer_list.html', context)


@admin_required
def freelancer_detail(request, user_id):
    """View freelancer details"""
    freelancer = get_object_or_404(User, id=user_id, user_type='freelancer')
    
    try:
        profile = freelancer.freelancer_profile
        # Split skills for template
        if profile and profile.skills:
            profile.skills_list = [skill.strip() for skill in profile.skills.split(',')]
        else:
            profile.skills_list = []
    except FreelancerProfile.DoesNotExist:
        profile = None
    
    # Get freelancer's services
    services = Service.objects.filter(freelancer=freelancer)
    
    # Get freelancer's bookings
    bookings = Booking.objects.filter(service__freelancer=freelancer).order_by('-created_at')[:10]
    
    context = {
        'freelancer': freelancer,
        'profile': profile,
        'services': services,
        'bookings': bookings,
    }
    
    return render(request, 'admin/freelancer_detail.html', context)


@admin_required
def approve_freelancer(request, user_id):
    """Approve a freelancer"""
    if request.method == 'POST':
        freelancer = get_object_or_404(User, id=user_id, user_type='freelancer')
        freelancer.is_verified = True
        freelancer.save()
        messages.success(request, f'{freelancer.get_full_name()} has been approved successfully!')
        
        # Check if there's a 'next' parameter to redirect back to list
        next_url = request.POST.get('next', request.GET.get('next'))
        if next_url:
            return redirect(next_url)
        return redirect('accounts:admin_freelancer_list')
    return redirect('accounts:admin_freelancer_list')


@admin_required
def reject_freelancer(request, user_id):
    """Reject/Suspend a freelancer"""
    if request.method == 'POST':
        freelancer = get_object_or_404(User, id=user_id, user_type='freelancer')
        freelancer.is_verified = False
        freelancer.is_active = False
        freelancer.save()
        messages.warning(request, f'{freelancer.get_full_name()} has been suspended.')
        return redirect('accounts:admin_freelancer_detail', user_id=user_id)
    return redirect('accounts:admin_freelancer_list')


@admin_required
def delete_freelancer(request, user_id):
    """Delete a freelancer account"""
    if request.method == 'POST':
        freelancer = get_object_or_404(User, id=user_id, user_type='freelancer')
        name = freelancer.get_full_name()
        freelancer.delete()
        messages.success(request, f'{name} has been deleted successfully.')
        return redirect('accounts:admin_freelancer_list')
    return redirect('accounts:admin_freelancer_list')


@admin_required
def toggle_freelancer_status(request, user_id):
    """Toggle freelancer active status"""
    if request.method == 'POST':
        freelancer = get_object_or_404(User, id=user_id, user_type='freelancer')
        freelancer.is_active = not freelancer.is_active
        freelancer.save()
        
        status = 'activated' if freelancer.is_active else 'deactivated'
        messages.success(request, f'{freelancer.get_full_name()} has been {status}.')
        
        return JsonResponse({'success': True, 'is_active': freelancer.is_active})
    
    return JsonResponse({'success': False}, status=400)


@admin_required
def user_list(request):
    """List all customers only"""
    search_query = request.GET.get('search', '')
    
    # Only show customers
    users = User.objects.filter(user_type='customer')
    
    # Apply search
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    users = users.order_by('-created_at')
    
    context = {
        'users': users,
        'search_query': search_query,
    }
    
    return render(request, 'admin/user_list.html', context)


@admin_required
def toggle_user_status(request, user_id):
    """Toggle user active status"""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.user_type == 'admin' or user.is_superuser:
            messages.error(request, 'Cannot modify admin users.')
            return redirect('accounts:admin_user_list')
        
        user.is_active = not user.is_active
        user.save()
        
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'{user.get_full_name()} has been {status}.')
        
        return redirect('accounts:admin_user_list')
    
    return redirect('accounts:admin_user_list')


@admin_required
def delete_user(request, user_id):
    """Delete a user account"""
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        if user.user_type == 'admin' or user.is_superuser:
            messages.error(request, 'Cannot delete admin users.')
            return redirect('accounts:admin_user_list')
        
        name = user.get_full_name()
        user.delete()
        messages.success(request, f'{name} has been deleted successfully.')
        return redirect('accounts:admin_user_list')
    
    return redirect('accounts:admin_user_list')


@admin_required
def service_list_admin(request):
    """List all services for admin approval"""
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Only show services from verified freelancers
    services = Service.objects.filter(
        freelancer__is_verified=True
    ).select_related('freelancer', 'category')
    
    # Apply filters
    if status_filter == 'pending':
        services = services.filter(is_approved=False)
    elif status_filter == 'approved':
        services = services.filter(is_approved=True)
    
    # Apply category filter
    if category_filter:
        services = services.filter(category_id=category_filter)
    
    # Apply search
    if search_query:
        services = services.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(freelancer__first_name__icontains=search_query) |
            Q(freelancer__last_name__icontains=search_query)
        )
    
    services = services.order_by('-created_at')
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'services': services,
        'status_filter': status_filter,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    
    return render(request, 'admin/service_list.html', context)


@admin_required
def approve_service(request, service_id):
    """Approve a service"""
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        service.is_approved = True
        service.save()
        messages.success(request, f'Service "{service.title}" has been approved!')
        
        # Check if there's a 'next' parameter to redirect back
        next_url = request.POST.get('next', request.GET.get('next'))
        if next_url:
            return redirect(next_url)
        return redirect('accounts:admin_service_list')
    return redirect('accounts:admin_service_list')


@admin_required
def reject_service(request, service_id):
    """Reject/Unapprove a service"""
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        service.is_approved = False
        service.save()
        messages.warning(request, f'Service "{service.title}" has been rejected!')
        return redirect('accounts:admin_service_list')
    return redirect('accounts:admin_service_list')


@admin_required
def delete_service(request, service_id):
    """Delete a service"""
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        title = service.title
        service.delete()
        messages.success(request, f'Service "{title}" has been deleted!')
        return redirect('accounts:admin_service_list')
    return redirect('accounts:admin_service_list')


@admin_required
def category_list_admin(request):
    """List all categories for admin management"""
    categories = Category.objects.all().order_by('name')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'admin/category_list.html', context)


@admin_required
def add_category(request):
    """Add a new category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            category = Category.objects.create(
                name=name,
                description=description,
                is_active=True
            )
            messages.success(request, f'Category "{name}" has been created successfully!')
            return redirect('accounts:admin_category_list')
        else:
            messages.error(request, 'Category name is required.')
    
    return render(request, 'admin/add_category.html')


@admin_required
def edit_category(request, category_id):
    """Edit a category"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.description = request.POST.get('description', category.description)
        category.is_active = request.POST.get('is_active') == 'on'
        category.save()
        
        messages.success(request, f'Category "{category.name}" has been updated!')
        return redirect('accounts:admin_category_list')
    
    context = {
        'category': category,
    }
    
    return render(request, 'admin/edit_category.html', context)


@admin_required
def delete_category(request, category_id):
    """Delete a category"""
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" has been deleted!')
        return redirect('accounts:admin_category_list')
    return redirect('accounts:admin_category_list')


@admin_required
def toggle_category_status(request, category_id):
    """Toggle category active status"""
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.is_active = not category.is_active
        category.save()
        
        status = 'activated' if category.is_active else 'deactivated'
        messages.success(request, f'Category "{category.name}" has been {status}!')
        return redirect('accounts:admin_category_list')
    return redirect('accounts:admin_category_list')
