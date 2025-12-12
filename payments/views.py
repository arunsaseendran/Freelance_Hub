from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment
from bookings.models import Booking

@login_required
def payment_page(request, booking_id):
    """Payment page for GPay"""
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    payment = get_object_or_404(Payment, booking=booking)
    
    if payment.status == 'completed':
        messages.info(request, 'Payment already completed.')
        return redirect('bookings:booking_detail', pk=booking.id)
    
    freelancer_profile = booking.freelancer.freelancer_profile
    
    context = {
        'booking': booking,
        'payment': payment,
        'freelancer_profile': freelancer_profile,
    }
    
    return render(request, 'payments/payment_page.html', context)


@login_required
def confirm_payment(request, payment_id):
    """Confirm GPay payment"""
    payment = get_object_or_404(Payment, pk=payment_id, customer=request.user)
    
    if request.method == 'POST':
        transaction_id = request.POST.get('transaction_id', '')
        
        if transaction_id:
            payment.mark_completed(transaction_id)
            messages.success(request, 'Payment confirmed successfully!')
            return redirect('bookings:booking_detail', pk=payment.booking.id)
        else:
            messages.error(request, 'Please enter transaction ID.')
            return redirect('payments:payment_page', booking_id=payment.booking.id)
    
    return redirect('payments:payment_page', booking_id=payment.booking.id)


@login_required
def payment_history(request):
    """View payment history"""
    if request.user.user_type == 'customer':
        payments = Payment.objects.filter(customer=request.user).select_related('booking')
    elif request.user.user_type == 'freelancer':
        payments = Payment.objects.filter(booking__freelancer=request.user).select_related('booking', 'customer')
    else:
        payments = Payment.objects.all().select_related('booking', 'customer')
    
    context = {
        'payments': payments,
    }
    
    return render(request, 'payments/payment_history.html', context)


