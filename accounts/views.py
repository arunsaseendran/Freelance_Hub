from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Sum, Avg, Q
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, FreelancerProfileForm, OTPVerificationForm
from .models import User, FreelancerProfile, EmailOTP
from .utils import send_otp_email, verify_otp
from bookings.models import Booking
from payments.models import Payment, Refund
from services.models import Service

def register(request):
    """User registration view with OTP verification"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Store form data in session for OTP verification
            request.session['registration_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password1': form.cleaned_data['password1'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'phone': form.cleaned_data['phone'],
                'user_type': form.cleaned_data['user_type'],
                'city': form.cleaned_data['city'],
                'area': form.cleaned_data['area'],
                'pincode': form.cleaned_data['pincode'],
                'address': form.cleaned_data['address'],
            }
            
            # Send OTP
            success, message = send_otp_email(form.cleaned_data['email'])
            if success:
                messages.success(request, 'Registration details saved! Please check your email for OTP verification.')
                return redirect('accounts:verify_otp')
            else:
                messages.error(request, f'Failed to send OTP: {message}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def verify_otp(request):
    """OTP verification view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    # Check if registration data exists in session
    if 'registration_data' not in request.session:
        messages.error(request, 'No registration data found. Please register again.')
        return redirect('accounts:register')
    
    registration_data = request.session['registration_data']
    email = registration_data['email']
    
    if request.method == 'POST':
        form = OTPVerificationForm(email, request.POST)
        if form.is_valid():
            # OTP is valid, create the user
            try:
                user = User.objects.create_user(
                    username=registration_data['username'],
                    email=registration_data['email'],
                    password=registration_data['password1'],
                    first_name=registration_data['first_name'],
                    last_name=registration_data['last_name'],
                    phone=registration_data['phone'],
                    user_type=registration_data['user_type'],
                    city=registration_data['city'],
                    area=registration_data['area'],
                    pincode=registration_data['pincode'],
                    address=registration_data['address'],
                )
                
                # Clear session data
                del request.session['registration_data']
                
                # Login the user
                login(request, user)
                messages.success(request, f'Welcome {user.username}! Your account has been created and verified.')
                return redirect('accounts:dashboard')
                
            except Exception as e:
                messages.error(request, f'Failed to create account: {str(e)}')
    else:
        form = OTPVerificationForm(email)
    
    return render(request, 'accounts/verify_otp.html', {
        'form': form,
        'email': email
    })


def resend_otp(request):
    """Resend OTP to email"""
    if request.method == 'POST':
        if 'registration_data' not in request.session:
            return JsonResponse({'success': False, 'message': 'No registration data found'})
        
        email = request.session['registration_data']['email']
        success, message = send_otp_email(email)
        
        return JsonResponse({
            'success': success,
            'message': message
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('accounts:dashboard')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """Main dashboard - redirects based on user type"""
    if request.user.user_type == 'admin' or request.user.is_superuser:
        return redirect('accounts:admin_dash')  # Redirect to custom admin dashboard
    elif request.user.user_type == 'freelancer':
        return redirect('accounts:freelancer_dashboard')
    else:
        return redirect('accounts:customer_dashboard')


@login_required
def admin_dashboard(request):
    """Old admin dashboard - redirects to new custom admin dashboard"""
    if not (request.user.user_type == 'admin' or request.user.is_superuser):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Redirect to the new custom admin dashboard
    return redirect('accounts:admin_dash')


@login_required
def freelancer_dashboard(request):
    """Freelancer dashboard"""
    if request.user.user_type != 'freelancer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    profile = request.user.freelancer_profile
    my_services = Service.objects.filter(freelancer=request.user)
    
    # Booking statistics
    total_bookings = Booking.objects.filter(freelancer=request.user).count()
    pending_bookings = Booking.objects.filter(freelancer=request.user, status='pending')
    accepted_bookings = Booking.objects.filter(freelancer=request.user, status='accepted')
    completed_bookings = Booking.objects.filter(freelancer=request.user, status='completed').count()
    
    # Revenue
    total_earnings = Payment.objects.filter(
        booking__freelancer=request.user,
        status='completed'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'profile': profile,
        'my_services': my_services,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'accepted_bookings': accepted_bookings,
        'completed_bookings': completed_bookings,
        'total_earnings': total_earnings,
    }
    
    return render(request, 'accounts/freelancer_dashboard.html', context)


@login_required
def customer_dashboard(request):
    """Customer dashboard"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    # Booking statistics
    my_bookings = Booking.objects.filter(customer=request.user).select_related('service', 'freelancer')
    pending_bookings = my_bookings.filter(status='pending')
    accepted_bookings = my_bookings.filter(status='accepted')
    completed_bookings = my_bookings.filter(status='completed')
    
    context = {
        'my_bookings': my_bookings[:10],
        'pending_bookings': pending_bookings,
        'accepted_bookings': accepted_bookings,
        'completed_bookings': completed_bookings,
    }
    
    return render(request, 'accounts/customer_dashboard.html', context)


@login_required
def profile(request):
    """View and edit user profile"""
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        
        if request.user.user_type == 'freelancer':
            freelancer_form = FreelancerProfileForm(request.POST, instance=request.user.freelancer_profile)
            if user_form.is_valid() and freelancer_form.is_valid():
                user_form.save()
                freelancer_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
        else:
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        freelancer_form = FreelancerProfileForm(instance=request.user.freelancer_profile) if request.user.user_type == 'freelancer' else None
    
    context = {
        'user_form': user_form,
        'freelancer_form': freelancer_form,
    }
    
    return render(request, 'accounts/profile.html', context)


def freelancer_list(request):
    """List all freelancers"""
    freelancers = User.objects.filter(user_type='freelancer', is_active=True).select_related('freelancer_profile')
    
    # Filter by location
    city = request.GET.get('city')
    area = request.GET.get('area')
    pincode = request.GET.get('pincode')
    
    if city:
        freelancers = freelancers.filter(city__icontains=city)
    if area:
        freelancers = freelancers.filter(area__icontains=area)
    if pincode:
        freelancers = freelancers.filter(pincode=pincode)
    
    context = {
        'freelancers': freelancers,
    }
    
    return render(request, 'accounts/freelancer_list.html', context)


def freelancer_detail(request, pk):
    """View freelancer profile details"""
    freelancer = get_object_or_404(User, pk=pk, user_type='freelancer')
    profile = freelancer.freelancer_profile
    services = Service.objects.filter(freelancer=freelancer, is_active=True)
    reviews = freelancer.reviews_received.filter(is_active=True).select_related('customer')[:10]
    
    # Split skills into a list for template rendering
    skills_list = []
    if profile.skills:
        skills_list = [skill.strip() for skill in profile.skills.split(',') if skill.strip()]
    
    context = {
        'freelancer': freelancer,
        'profile': profile,
        'services': services,
        'reviews': reviews,
        'skills_list': skills_list,
    }
    
    return render(request, 'accounts/freelancer_detail.html', context)


@login_required
def delete_account(request):
    """Delete user account and all related data"""
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        
        # Verify password
        if not user.check_password(password):
            messages.error(request, 'Incorrect password. Account deletion cancelled.')
            return redirect('accounts:delete_account')
        
        # Store username for message
        username = user.username
        
        # Django's CASCADE will automatically delete related objects:
        # - For customers: bookings, payments, reviews, refunds
        # - For freelancers: services, bookings (as freelancer), payments received
        # - FreelancerProfile will be deleted due to OneToOne relationship
        
        # Logout user
        logout(request)
        
        # Delete user (this cascades to all related data)
        user.delete()
        
        messages.success(request, f'Account "{username}" has been permanently deleted along with all associated data.')
        return redirect('home')
    
    return render(request, 'accounts/delete_account.html')
