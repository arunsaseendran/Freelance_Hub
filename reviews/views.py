from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, ReviewResponse
from .forms import ReviewForm, ReviewResponseForm
from bookings.models import Booking

@login_required
def create_review(request, booking_id):
    """Customer creates review after service completion"""
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user, status='completed')
    
    # Check if review already exists
    if hasattr(booking, 'review'):
        messages.info(request, 'You have already reviewed this service.')
        return redirect('bookings:booking_detail', pk=booking.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.customer = request.user
            review.freelancer = booking.freelancer
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('bookings:booking_detail', pk=booking.id)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'booking': booking,
    }
    
    return render(request, 'reviews/create_review.html', context)


@login_required
def edit_review(request, review_id):
    """Edit existing review"""
    review = get_object_or_404(Review, pk=review_id, customer=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully!')
            return redirect('bookings:booking_detail', pk=review.booking.id)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'form': form,
        'review': review,
    }
    
    return render(request, 'reviews/edit_review.html', context)


@login_required
def delete_review(request, review_id):
    """Delete review"""
    review = get_object_or_404(Review, pk=review_id, customer=request.user)
    booking_id = review.booking.id
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('bookings:booking_detail', pk=booking_id)
    
    context = {
        'review': review,
    }
    
    return render(request, 'reviews/delete_review.html', context)


@login_required
def respond_to_review(request, review_id):
    """Freelancer responds to review"""
    review = get_object_or_404(Review, pk=review_id, freelancer=request.user)
    
    # Check if response already exists
    if hasattr(review, 'response'):
        messages.info(request, 'You have already responded to this review.')
        return redirect('accounts:freelancer_dashboard')
    
    if request.method == 'POST':
        form = ReviewResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.review = review
            response.freelancer = request.user
            response.save()
            messages.success(request, 'Response submitted successfully!')
            return redirect('accounts:freelancer_dashboard')
    else:
        form = ReviewResponseForm()
    
    context = {
        'form': form,
        'review': review,
    }
    
    return render(request, 'reviews/respond_to_review.html', context)


def freelancer_reviews(request, freelancer_id):
    """View all reviews for a freelancer"""
    from accounts.models import User
    freelancer = get_object_or_404(User, pk=freelancer_id, user_type='freelancer')
    reviews = Review.objects.filter(freelancer=freelancer, is_active=True).select_related('customer', 'booking')
    
    context = {
        'freelancer': freelancer,
        'reviews': reviews,
    }
    
    return render(request, 'reviews/freelancer_reviews.html', context)
