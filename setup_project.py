#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script to initialize the Freelancer Service Booking Platform
Run this after installing requirements and running migrations
"""

import os
import sys
import django

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancer_platform.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import Category, SubCategory

User = get_user_model()

def create_superuser():
    """Create a superuser if it doesn't exist"""
    if not User.objects.filter(username='admin').exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            username='admin',
            email='admin@freelancehub.com',
            password='admin123',
            user_type='admin',
            first_name='Admin',
            last_name='User'
        )
        print("✓ Superuser created (username: admin, password: admin123)")
    else:
        print("✓ Superuser already exists")

def create_categories():
    """Create default service categories"""
    categories_data = [
        {
            'name': 'Home Cleaning',
            'description': 'Professional home cleaning services',
            'subcategories': ['Deep Cleaning', 'Regular Cleaning', 'Move-in/Move-out Cleaning']
        },
        {
            'name': 'Electrical Work',
            'description': 'Electrical installation and repair services',
            'subcategories': ['Wiring', 'Appliance Repair', 'Installation']
        },
        {
            'name': 'Beauty Care',
            'description': 'Beauty and personal care services',
            'subcategories': ['Hair Styling', 'Makeup', 'Spa Services', 'Nail Care']
        },
        {
            'name': 'Plumbing',
            'description': 'Plumbing services and repairs',
            'subcategories': ['Pipe Repair', 'Installation', 'Drain Cleaning']
        },
        {
            'name': 'Tutoring',
            'description': 'Educational tutoring services',
            'subcategories': ['Mathematics', 'Science', 'Languages', 'Computer Science']
        },
        {
            'name': 'Carpentry',
            'description': 'Woodwork and furniture services',
            'subcategories': ['Furniture Repair', 'Custom Furniture', 'Installation']
        },
        {
            'name': 'Painting',
            'description': 'Interior and exterior painting services',
            'subcategories': ['Interior Painting', 'Exterior Painting', 'Wall Design']
        },
        {
            'name': 'Gardening',
            'description': 'Garden maintenance and landscaping',
            'subcategories': ['Lawn Care', 'Plant Care', 'Landscaping']
        },
        {
            'name': 'Graphic Design',
            'description': 'Professional graphic design services',
            'subcategories': ['Logo Design', 'Branding', 'Social Media Graphics', 'Print Design']
        },
        {
            'name': 'Web Development',
            'description': 'Website and web application development',
            'subcategories': ['Frontend Development', 'Backend Development', 'Full Stack', 'WordPress']
        },
        {
            'name': 'Content Writing',
            'description': 'Professional content writing services',
            'subcategories': ['Blog Writing', 'Copywriting', 'Technical Writing', 'SEO Content']
        },
        {
            'name': 'Digital Marketing',
            'description': 'Digital marketing and SEO services',
            'subcategories': ['SEO', 'Social Media Marketing', 'Email Marketing', 'PPC Advertising']
        },
        {
            'name': 'Video Editing',
            'description': 'Professional video editing services',
            'subcategories': ['YouTube Videos', 'Corporate Videos', 'Social Media Videos', 'Animation']
        }
    ]
    
    print("\nCreating service categories...")
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✓ Created category: {cat_data['name']}")
            
            # Create subcategories
            for sub_name in cat_data['subcategories']:
                SubCategory.objects.get_or_create(
                    category=category,
                    name=sub_name
                )
            print(f"  Added {len(cat_data['subcategories'])} subcategories")
        else:
            print(f"✓ Category already exists: {cat_data['name']}")

def create_sample_users():
    """Create sample freelancer and customer accounts"""
    print("\nCreating sample users...")
    
    # Sample Customer
    if not User.objects.filter(username='customer1').exists():
        customer = User.objects.create_user(
            username='customer1',
            email='customer@example.com',
            password='customer123',
            user_type='customer',
            first_name='John',
            last_name='Doe',
            phone='9876543210',
            city='Mumbai',
            area='Andheri',
            pincode='400053',
            address='123 Sample Street'
        )
        print("✓ Sample customer created (username: customer1, password: customer123)")
    else:
        print("✓ Sample customer already exists")
    
    # Sample Freelancer
    if not User.objects.filter(username='freelancer1').exists():
        freelancer = User.objects.create_user(
            username='freelancer1',
            email='freelancer@example.com',
            password='freelancer123',
            user_type='freelancer',
            first_name='Jane',
            last_name='Smith',
            phone='9876543211',
            city='Mumbai',
            area='Bandra',
            pincode='400050',
            address='456 Service Lane'
        )
        
        # Update freelancer profile
        profile = freelancer.freelancer_profile
        profile.bio = "Experienced professional with 5+ years in the industry"
        profile.experience_years = 5
        profile.skills = "Cleaning, Organization, Time Management"
        profile.payment_mode = 'both'
        profile.gpay_number = '9876543211'
        profile.hourly_rate = 500
        profile.is_available = True
        profile.save()
        
        print("✓ Sample freelancer created (username: freelancer1, password: freelancer123)")
    else:
        print("✓ Sample freelancer already exists")

def main():
    """Main setup function"""
    print("=" * 60)
    print("Freelancer Service Booking Platform - Initial Setup")
    print("=" * 60)
    
    try:
        create_superuser()
        create_categories()
        create_sample_users()
        
        print("\n" + "=" * 60)
        print("Setup completed successfully!")
        print("=" * 60)
        print("\nYou can now run the development server:")
        print("  python manage.py runserver")
        print("\nAccess the application at: http://127.0.0.1:8000/")
        print("Admin panel at: http://127.0.0.1:8000/admin/")
        print("\nDefault credentials:")
        print("  Admin: admin / admin123")
        print("  Customer: customer1 / customer123")
        print("  Freelancer: freelancer1 / freelancer123")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during setup: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
