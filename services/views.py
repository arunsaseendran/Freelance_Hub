from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Service, Category, SubCategory
from .forms import ServiceForm, ServiceSearchForm

def service_list(request):
    """List all services with search and filters"""
    # Only show approved services from verified freelancers
    services = Service.objects.filter(
        is_active=True,
        is_approved=True,
        freelancer__is_verified=True
    ).select_related('freelancer', 'category', 'subcategory')
    form = ServiceSearchForm(request.GET)
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        city = form.cleaned_data.get('city')
        area = form.cleaned_data.get('area')
        pincode = form.cleaned_data.get('pincode')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        
        if query:
            services = services.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        
        if category:
            services = services.filter(category=category)
        
        if city:
            services = services.filter(freelancer__city__icontains=city)
        
        if area:
            services = services.filter(freelancer__area__icontains=area)
        
        if pincode:
            services = services.filter(freelancer__pincode=pincode)
        
        if min_price:
            services = services.filter(price__gte=min_price)
        
        if max_price:
            services = services.filter(price__lte=max_price)
    
    context = {
        'services': services,
        'form': form,
        'categories': Category.objects.filter(is_active=True),
    }
    
    return render(request, 'services/service_list.html', context)


def service_detail(request, pk):
    """View service details"""
    service = get_object_or_404(Service, pk=pk, is_active=True)
    freelancer = service.freelancer
    profile = freelancer.freelancer_profile
    other_services = Service.objects.filter(freelancer=freelancer, is_active=True).exclude(pk=pk)[:4]
    
    context = {
        'service': service,
        'freelancer': freelancer,
        'profile': profile,
        'other_services': other_services,
    }
    
    return render(request, 'services/service_detail.html', context)


@login_required
def my_services(request):
    """Freelancer's own services"""
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    services = Service.objects.filter(freelancer=request.user)
    
    context = {
        'services': services,
    }
    
    return render(request, 'services/my_services.html', context)


@login_required
def service_create(request):
    """Create new service"""
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Only freelancers can create services.')
        return redirect('home')
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.freelancer = request.user
            service.save()
            messages.success(request, 'Service created successfully!')
            return redirect('services:my_services')
    else:
        form = ServiceForm()
    
    context = {
        'form': form,
        'title': 'Create Service',
    }
    
    return render(request, 'services/service_form.html', context)


@login_required
def service_edit(request, pk):
    """Edit existing service"""
    service = get_object_or_404(Service, pk=pk, freelancer=request.user)
    
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service updated successfully!')
            return redirect('services:my_services')
    else:
        form = ServiceForm(instance=service)
    
    context = {
        'form': form,
        'service': service,
        'title': 'Edit Service',
    }
    
    return render(request, 'services/service_form.html', context)


@login_required
def service_delete(request, pk):
    """Delete service"""
    service = get_object_or_404(Service, pk=pk, freelancer=request.user)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect('services:my_services')
    
    context = {
        'service': service,
    }
    
    return render(request, 'services/service_confirm_delete.html', context)


def category_list(request):
    """List all categories"""
    categories = Category.objects.filter(is_active=True).prefetch_related('subcategories')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'services/category_list.html', context)


def category_services(request, pk):
    """Services in a specific category"""
    category = get_object_or_404(Category, pk=pk, is_active=True)
    # Only show approved services from verified freelancers
    services = Service.objects.filter(
        category=category,
        is_active=True,
        is_approved=True,
        freelancer__is_verified=True
    ).select_related('freelancer')
    
    context = {
        'category': category,
        'services': services,
    }
    
    return render(request, 'services/category_services.html', context)
