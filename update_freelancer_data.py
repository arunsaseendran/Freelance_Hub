#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to update freelancer profiles with random but realistic data:
- Rating (0.0 to 5.0)
- Experience (1 to 15 years)
- Hourly Rate (₹200 to ₹2000)
"""

import os
import sys
import django
import random
from decimal import Decimal

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancer_platform.settings')
django.setup()

from accounts.models import User, FreelancerProfile

def generate_rating():
    """Generate a realistic rating between 3.5 and 5.0"""
    # Most freelancers have good ratings (3.5-5.0)
    return round(random.uniform(3.5, 5.0), 2)

def generate_experience():
    """Generate experience years (1-15 years)"""
    # More freelancers have 2-8 years experience
    weights = [5, 10, 15, 20, 20, 15, 10, 5, 3, 2, 2, 1, 1, 1, 1]  # 1-15 years
    return random.choices(range(1, 16), weights=weights)[0]

def generate_hourly_rate(experience):
    """Generate hourly rate based on experience"""
    # Base rate increases with experience
    base_rates = {
        range(1, 3): (200, 400),    # 1-2 years: ₹200-400
        range(3, 5): (350, 600),    # 3-4 years: ₹350-600
        range(5, 8): (500, 900),    # 5-7 years: ₹500-900
        range(8, 12): (800, 1400),  # 8-11 years: ₹800-1400
        range(12, 20): (1200, 2000) # 12+ years: ₹1200-2000
    }
    
    for exp_range, (min_rate, max_rate) in base_rates.items():
        if experience in exp_range:
            return random.randint(min_rate, max_rate)
    
    return random.randint(200, 500)  # Default

def update_freelancer_profiles():
    """Update all freelancer profiles with random data"""
    print("=" * 70)
    print("Updating Freelancer Profiles with Random Data")
    print("=" * 70)
    print()
    
    # Get all freelancers
    freelancers = User.objects.filter(user_type='freelancer')
    
    if not freelancers.exists():
        print("❌ No freelancers found in database!")
        return
    
    print(f"Found {freelancers.count()} freelancer(s)\n")
    
    updated_count = 0
    
    for user in freelancers:
        try:
            # Get or create freelancer profile
            profile, created = FreelancerProfile.objects.get_or_create(user=user)
            
            # Generate random data
            experience = generate_experience()
            rating = generate_rating()
            hourly_rate = generate_hourly_rate(experience)
            
            # Update profile
            profile.experience_years = experience
            profile.rating = Decimal(str(rating))
            profile.hourly_rate = Decimal(str(hourly_rate))
            
            # Add some random skills if empty
            if not profile.skills or profile.skills.strip() == '':
                skill_sets = [
                    "Python, Django, Web Development",
                    "JavaScript, React, Node.js",
                    "Graphic Design, Photoshop, Illustrator",
                    "Content Writing, SEO, Copywriting",
                    "Video Editing, Premiere Pro, After Effects",
                    "Home Cleaning, Organization, Deep Cleaning",
                    "Electrical Work, Wiring, Repairs",
                    "Plumbing, Pipe Repair, Installation",
                    "Beauty Care, Hair Styling, Makeup",
                    "Carpentry, Furniture Making, Repairs"
                ]
                profile.skills = random.choice(skill_sets)
            
            # Add bio if empty
            if not profile.bio or profile.bio.strip() == '':
                bios = [
                    f"Experienced professional with {experience} years in the industry. Dedicated to delivering quality work.",
                    f"Skilled freelancer with {experience} years of experience. Customer satisfaction is my priority.",
                    f"Professional service provider with {experience} years of expertise. Quality guaranteed.",
                    f"{experience} years of experience delivering excellent results. Let's work together!",
                    f"Passionate about my work with {experience} years of hands-on experience."
                ]
                profile.bio = random.choice(bios)
            
            # Set availability
            profile.is_available = random.choice([True, True, True, False])  # 75% available
            
            # Save profile
            profile.save()
            
            # Display update
            print(f"✓ Updated: {user.get_full_name() or user.username}")
            print(f"  Location: {user.city}, {user.area}")
            print(f"  Experience: {experience} years")
            print(f"  Rating: {rating} ⭐")
            print(f"  Hourly Rate: ₹{hourly_rate}/hour")
            print(f"  Skills: {profile.skills[:50]}...")
            print(f"  Available: {'Yes' if profile.is_available else 'No'}")
            print()
            
            updated_count += 1
            
        except Exception as e:
            print(f"✗ Error updating {user.username}: {str(e)}")
            print()
    
    print("=" * 70)
    print(f"✓ Successfully updated {updated_count} freelancer profile(s)")
    print("=" * 70)
    print()
    
    # Display summary statistics
    print("Summary Statistics:")
    print("-" * 70)
    
    all_profiles = FreelancerProfile.objects.all()
    if all_profiles.exists():
        avg_rating = all_profiles.aggregate(models.Avg('rating'))['rating__avg']
        avg_experience = all_profiles.aggregate(models.Avg('experience_years'))['experience_years__avg']
        avg_rate = all_profiles.aggregate(models.Avg('hourly_rate'))['hourly_rate__avg']
        
        print(f"Average Rating: {avg_rating:.2f} ⭐")
        print(f"Average Experience: {avg_experience:.1f} years")
        print(f"Average Hourly Rate: ₹{avg_rate:.2f}/hour")
        print(f"Total Freelancers: {all_profiles.count()}")
        print(f"Available: {all_profiles.filter(is_available=True).count()}")
        print(f"Unavailable: {all_profiles.filter(is_available=False).count()}")
    
    print()

if __name__ == '__main__':
    # Import models for aggregation
    from django.db import models
    
    try:
        update_freelancer_profiles()
        print("✓ Update completed successfully!")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
