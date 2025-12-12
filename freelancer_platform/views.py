from django.shortcuts import render
from services.models import Category


def home(request):
    """Home page view with categories"""
    categories = Category.objects.filter(is_active=True)[:8]  # Show first 8 categories
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'home.html', context)
