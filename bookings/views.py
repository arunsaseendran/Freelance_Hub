from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from .models import Booking
from .forms import BookingForm, FreelancerNotesForm
from services.models import Service
from payments.models import Payment
import json

@login_required
def create_booking(request, service_id):
    """Create a new booking"""
    if request.user.user_type != 'customer':
        messages.error(request, 'Only customers can book services.')
        return redirect('services:service_detail', pk=service_id)
    
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    freelancer = service.freelancer
    profile = freelancer.freelancer_profile
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        payment_method = request.POST.get('payment_method')
        
        if form.is_valid():
            # Validate payment method
            if payment_method not in ['cash', 'razorpay']:
                messages.error(request, 'Invalid payment method.')
                return redirect('services:service_detail', pk=service_id)
            
            # Check if freelancer accepts this payment method (except razorpay which is always available)
            if payment_method == 'cash':
                if profile.payment_mode == 'gpay':
                    messages.error(request, 'This freelancer only accepts online payments.')
                    return redirect('services:service_detail', pk=service_id)
            
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.freelancer = freelancer
            booking.service = service
            booking.total_amount = service.price
            booking.save()
            
            # Handle Razorpay payment
            if payment_method == 'razorpay':
                # Get Razorpay payment details from form
                razorpay_payment_id = request.POST.get('razorpay_payment_id')
                razorpay_order_id = request.POST.get('razorpay_order_id')
                razorpay_signature = request.POST.get('razorpay_signature')
                
                if razorpay_payment_id:
                    # Payment was successful, create payment record
                    payment = Payment.objects.create(
                        booking=booking,
                        customer=request.user,
                        amount=service.price,
                        payment_method='razorpay',
                        status='completed',
                        transaction_id=razorpay_payment_id,
                        payment_details=json.dumps({
                            'razorpay_payment_id': razorpay_payment_id,
                            'razorpay_order_id': razorpay_order_id,
                            'razorpay_signature': razorpay_signature
                        })
                    )
                    # Keep booking as 'pending' so freelancer sees it in their pending bookings
                    messages.success(request, 'Booking created! Payment successful. Waiting for freelancer acceptance.')
                else:
                    # Payment failed or cancelled
                    booking.delete()
                    messages.error(request, 'Payment failed. Please try again.')
                    return redirect('services:service_detail', pk=service_id)
            else:
                # Create payment record for other methods
                payment = Payment.objects.create(
                    booking=booking,
                    customer=request.user,
                    amount=service.price,
                    payment_method=payment_method,
                    status='pending'
                )
                messages.success(request, 'Booking created successfully!')
            
            return redirect('bookings:booking_detail', pk=booking.id)
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'service': service,
        'freelancer': freelancer,
        'profile': profile,
    }
    
    return render(request, 'bookings/create_booking.html', context)


@login_required
def booking_detail(request, pk):
    """View booking details"""
    booking = get_object_or_404(Booking, pk=pk)
    
    # Check permissions
    if booking.customer != request.user and booking.freelancer != request.user:
        if not (request.user.is_superuser or request.user.user_type == 'admin'):
            messages.error(request, 'Access denied.')
            return redirect('home')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/booking_detail.html', context)


@login_required
def my_bookings(request):
    """List user's bookings"""
    if request.user.user_type == 'customer':
        bookings = Booking.objects.filter(customer=request.user).select_related('service', 'freelancer')
    elif request.user.user_type == 'freelancer':
        bookings = Booking.objects.filter(freelancer=request.user).select_related('service', 'customer')
    else:
        bookings = Booking.objects.all().select_related('service', 'customer', 'freelancer')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    
    context = {
        'bookings': bookings,
    }
    
    return render(request, 'bookings/my_bookings.html', context)


@login_required
def accept_booking(request, pk):
    """Freelancer accepts booking"""
    booking = get_object_or_404(Booking, pk=pk, freelancer=request.user)
    
    if request.method == 'POST':
        if booking.accept_booking():
            messages.success(request, 'Booking accepted successfully!')
        else:
            messages.error(request, 'Cannot accept this booking.')
        return redirect('bookings:booking_detail', pk=pk)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/accept_booking.html', context)


@login_required
def reject_booking(request, pk):
    """Freelancer rejects booking"""
    booking = get_object_or_404(Booking, pk=pk, freelancer=request.user)
    
    if request.method == 'POST':
        if booking.reject_booking():
            messages.success(request, 'Booking rejected.')
        else:
            messages.error(request, 'Cannot reject this booking.')
        return redirect('bookings:my_bookings')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/reject_booking.html', context)


@login_required
def complete_booking(request, pk):
    """Freelancer marks booking as completed"""
    booking = get_object_or_404(Booking, pk=pk, freelancer=request.user)
    
    if request.method == 'POST':
        form = FreelancerNotesForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            if booking.complete_booking():
                # Mark cash payment as completed
                if hasattr(booking, 'payment') and booking.payment.payment_method == 'cash':
                    booking.payment.mark_completed()
                messages.success(request, 'Booking marked as completed!')
            else:
                messages.error(request, 'Cannot complete this booking.')
            return redirect('bookings:booking_detail', pk=pk)
    else:
        form = FreelancerNotesForm(instance=booking)
    
    context = {
        'booking': booking,
        'form': form,
    }
    
    return render(request, 'bookings/complete_booking.html', context)


@login_required
def cancel_booking(request, pk):
    """Customer cancels booking"""
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    
    if not booking.can_cancel():
        cancellation_minutes = int(settings.BOOKING_CANCELLATION_HOURS * 60)
        messages.error(request, f'Cannot cancel booking. Cancellation is only allowed up to {cancellation_minutes} minutes before the scheduled time.')
        return redirect('bookings:booking_detail', pk=pk)
    
    if request.method == 'POST':
        if booking.cancel_booking():
            messages.success(request, 'Booking cancelled successfully!')
            return redirect('bookings:my_bookings')
        else:
            messages.error(request, 'Cannot cancel this booking.')
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/cancel_booking.html', context)
