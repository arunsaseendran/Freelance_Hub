"""
Script to add Kerala-based freelancers with native names and services
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancer_platform.settings')
django.setup()

from accounts.models import User, FreelancerProfile
from services.models import Service, Category, SubCategory

# Kerala cities and areas
kerala_locations = [
    {'city': 'Kochi', 'area': 'Edappally', 'pincode': '682024'},
    {'city': 'Kochi', 'area': 'Kakkanad', 'pincode': '682030'},
    {'city': 'Thiruvananthapuram', 'area': 'Pattom', 'pincode': '695004'},
    {'city': 'Thiruvananthapuram', 'area': 'Kazhakootam', 'pincode': '695582'},
    {'city': 'Kozhikode', 'area': 'Mavoor Road', 'pincode': '673004'},
    {'city': 'Kozhikode', 'area': 'Hilite City', 'pincode': '673014'},
    {'city': 'Thrissur', 'area': 'Swaraj Round', 'pincode': '680001'},
    {'city': 'Kannur', 'area': 'Thalassery', 'pincode': '670101'},
    {'city': 'Kollam', 'area': 'Chinnakada', 'pincode': '691001'},
    {'city': 'Palakkad', 'area': 'Fort Maidan', 'pincode': '678001'},
    {'city': 'Malappuram', 'area': 'Manjeri', 'pincode': '676121'},
    {'city': 'Kottayam', 'area': 'MC Road', 'pincode': '686001'},
]

# Kerala freelancers data
freelancers_data = [
    {
        'username': 'rajesh_electrician',
        'first_name': 'Rajesh',
        'last_name': 'Kumar',
        'email': 'rajesh.kumar@example.com',
        'phone': '9876543210',
        'password': 'freelancer123',
        'location': kerala_locations[0],
        'services': [
            {'category': 'Electrical Work', 'title': 'Home Electrical Repairs', 'description': 'Expert in home wiring, fan installation, and electrical troubleshooting. 10+ years experience.', 'price': 500, 'duration': 120},
            {'category': 'Electrical Work', 'title': 'AC Installation & Repair', 'description': 'Professional AC installation, servicing and repair for all brands.', 'price': 800, 'duration': 180},
        ]
    },
    {
        'username': 'sreelakshmi_beauty',
        'first_name': 'Sreelakshmi',
        'last_name': 'Nair',
        'email': 'sreelakshmi.nair@example.com',
        'phone': '9876543211',
        'password': 'freelancer123',
        'location': kerala_locations[1],
        'services': [
            {'category': 'Beauty Care', 'title': 'Bridal Makeup', 'description': 'Traditional Kerala bridal makeup with modern touch. Specialized in South Indian bridal looks.', 'price': 5000, 'duration': 180},
            {'category': 'Beauty Care', 'title': 'Hair Styling & Spa', 'description': 'Professional hair styling, spa treatments, and hair care services at home.', 'price': 1500, 'duration': 120},
        ]
    },
    {
        'username': 'arun_plumber',
        'first_name': 'Arun',
        'last_name': 'Krishnan',
        'email': 'arun.krishnan@example.com',
        'phone': '9876543212',
        'password': 'freelancer123',
        'location': kerala_locations[2],
        'services': [
            {'category': 'Plumbing', 'title': 'Plumbing Repairs', 'description': 'All types of plumbing work - pipe leaks, bathroom fittings, water tank installation.', 'price': 600, 'duration': 90},
            {'category': 'Plumbing', 'title': 'Bathroom Renovation', 'description': 'Complete bathroom plumbing renovation and modern fitting installation.', 'price': 3000, 'duration': 480},
        ]
    },
    {
        'username': 'divya_tutor',
        'first_name': 'Divya',
        'last_name': 'Menon',
        'email': 'divya.menon@example.com',
        'phone': '9876543213',
        'password': 'freelancer123',
        'location': kerala_locations[3],
        'services': [
            {'category': 'Tutoring', 'title': 'Mathematics Tuition (Class 8-12)', 'description': 'Expert mathematics tutor for CBSE/State board. Specialized in board exam preparation.', 'price': 800, 'duration': 60},
            {'category': 'Tutoring', 'title': 'Science Tuition', 'description': 'Physics, Chemistry, Biology tuition for high school students. Concept-based teaching.', 'price': 900, 'duration': 60},
        ]
    },
    {
        'username': 'muhammed_carpenter',
        'first_name': 'Muhammed',
        'last_name': 'Rasheed',
        'email': 'muhammed.rasheed@example.com',
        'phone': '9876543214',
        'password': 'freelancer123',
        'location': kerala_locations[4],
        'services': [
            {'category': 'Carpentry', 'title': 'Furniture Repair', 'description': 'Expert furniture repair and restoration. Specializing in traditional Kerala wood work.', 'price': 700, 'duration': 120},
            {'category': 'Carpentry', 'title': 'Custom Furniture Making', 'description': 'Custom-made furniture design and creation. Traditional and modern styles.', 'price': 5000, 'duration': 480},
        ]
    },
    {
        'username': 'priya_cleaner',
        'first_name': 'Priya',
        'last_name': 'Varghese',
        'email': 'priya.varghese@example.com',
        'phone': '9876543215',
        'password': 'freelancer123',
        'location': kerala_locations[5],
        'services': [
            {'category': 'Home Cleaning', 'title': 'Deep House Cleaning', 'description': 'Complete house deep cleaning including kitchen, bathrooms, and all rooms.', 'price': 1200, 'duration': 240},
            {'category': 'Home Cleaning', 'title': 'Kitchen Cleaning', 'description': 'Professional kitchen cleaning with eco-friendly products. Chimney and stove cleaning included.', 'price': 600, 'duration': 120},
        ]
    },
    {
        'username': 'suresh_painter',
        'first_name': 'Suresh',
        'last_name': 'Pillai',
        'email': 'suresh.pillai@example.com',
        'phone': '9876543216',
        'password': 'freelancer123',
        'location': kerala_locations[6],
        'services': [
            {'category': 'Painting', 'title': 'Interior House Painting', 'description': 'Professional interior painting with premium quality paints. Color consultation included.', 'price': 8000, 'duration': 480},
            {'category': 'Painting', 'title': 'Exterior Painting', 'description': 'Weather-resistant exterior painting for homes and buildings.', 'price': 12000, 'duration': 600},
        ]
    },
    {
        'username': 'anjali_designer',
        'first_name': 'Anjali',
        'last_name': 'Suresh',
        'email': 'anjali.suresh@example.com',
        'phone': '9876543217',
        'password': 'freelancer123',
        'location': kerala_locations[7],
        'services': [
            {'category': 'Beauty Care', 'title': 'Mehendi Design', 'description': 'Traditional and modern mehendi designs for weddings and festivals. Kerala style specialty.', 'price': 1500, 'duration': 120},
            {'category': 'Beauty Care', 'title': 'Saree Draping', 'description': 'Professional saree draping in various Kerala and South Indian styles.', 'price': 500, 'duration': 30},
        ]
    },
    {
        'username': 'vineeth_mechanic',
        'first_name': 'Vineeth',
        'last_name': 'Thomas',
        'email': 'vineeth.thomas@example.com',
        'phone': '9876543218',
        'password': 'freelancer123',
        'location': kerala_locations[8],
        'services': [
            {'category': 'Appliance Repair', 'title': 'Washing Machine Repair', 'description': 'Expert repair for all brands of washing machines. Quick and reliable service.', 'price': 500, 'duration': 90},
            {'category': 'Appliance Repair', 'title': 'Refrigerator Repair', 'description': 'Professional refrigerator repair and gas refilling service.', 'price': 800, 'duration': 120},
        ]
    },
    {
        'username': 'lakshmi_cook',
        'first_name': 'Lakshmi',
        'last_name': 'Devi',
        'email': 'lakshmi.devi@example.com',
        'phone': '9876543219',
        'password': 'freelancer123',
        'location': kerala_locations[9],
        'services': [
            {'category': 'Catering', 'title': 'Kerala Sadya Catering', 'description': 'Authentic Kerala sadya preparation for functions and festivals. Traditional recipes.', 'price': 300, 'duration': 180},
            {'category': 'Catering', 'title': 'Home Cooking Service', 'description': 'Daily home cooking service - Kerala cuisine specialty. Healthy and hygienic.', 'price': 5000, 'duration': 120},
        ]
    },
    {
        'username': 'ravi_gardener',
        'first_name': 'Ravi',
        'last_name': 'Chandran',
        'email': 'ravi.chandran@example.com',
        'phone': '9876543220',
        'password': 'freelancer123',
        'location': kerala_locations[10],
        'services': [
            {'category': 'Gardening', 'title': 'Garden Maintenance', 'description': 'Complete garden maintenance - pruning, weeding, lawn care. Kerala tropical plants expert.', 'price': 800, 'duration': 180},
            {'category': 'Gardening', 'title': 'Terrace Garden Setup', 'description': 'Design and setup of terrace gardens with Kerala native plants and vegetables.', 'price': 3000, 'duration': 240},
        ]
    },
    {
        'username': 'reshma_tailor',
        'first_name': 'Reshma',
        'last_name': 'Beevi',
        'email': 'reshma.beevi@example.com',
        'phone': '9876543221',
        'password': 'freelancer123',
        'location': kerala_locations[11],
        'services': [
            {'category': 'Tailoring', 'title': 'Blouse Stitching', 'description': 'Custom blouse stitching for sarees. Traditional and modern designs. Perfect fitting guaranteed.', 'price': 500, 'duration': 120},
            {'category': 'Tailoring', 'title': 'Churidar & Salwar Stitching', 'description': 'Expert stitching of churidar, salwar kameez, and traditional Kerala dress.', 'price': 600, 'duration': 180},
        ]
    },
]

def create_kerala_freelancers():
    print("Adding Kerala-based freelancers...")
    
    created_count = 0
    
    for freelancer_data in freelancers_data:
        # Check if user already exists
        if User.objects.filter(username=freelancer_data['username']).exists():
            print(f"WARNING: User {freelancer_data['username']} already exists, skipping...")
            continue
        
        # Create freelancer user
        location = freelancer_data['location']
        user = User.objects.create_user(
            username=freelancer_data['username'],
            email=freelancer_data['email'],
            password=freelancer_data['password'],
            first_name=freelancer_data['first_name'],
            last_name=freelancer_data['last_name'],
            phone=freelancer_data['phone'],
            user_type='freelancer',
            city=location['city'],
            area=location['area'],
            pincode=location['pincode'],
            address=f"{location['area']}, {location['city']}, Kerala"
        )
        
        # Create or update freelancer profile
        profile, created = FreelancerProfile.objects.get_or_create(
            user=user,
            defaults={
                'payment_mode': 'both',
                'bio': f"Professional service provider from {location['city']}, Kerala",
                'experience_years': 5,
                'skills': 'Professional, Reliable, Quality Service',
                'is_available': True
            }
        )
        
        print(f"SUCCESS: Created freelancer: {user.get_full_name()} ({user.username})")
        
        # Create services for this freelancer
        for service_data in freelancer_data['services']:
            try:
                category = Category.objects.get(name=service_data['category'])
                
                service = Service.objects.create(
                    freelancer=user,
                    category=category,
                    title=service_data['title'],
                    description=service_data['description'],
                    price=service_data['price'],
                    duration=service_data['duration'],
                    is_active=True
                )
                
                print(f"   - Added service: {service.title}")
                
            except Category.DoesNotExist:
                print(f"   WARNING: Category '{service_data['category']}' not found, skipping service...")
        
        created_count += 1
    
    print(f"\nSUCCESS: Added {created_count} Kerala-based freelancers!")
    print(f"Locations covered: Kochi, Thiruvananthapuram, Kozhikode, Thrissur, Kannur, Kollam, Palakkad, Malappuram, Kottayam")
    print(f"\nLogin credentials for all freelancers:")
    print(f"   Password: freelancer123")

if __name__ == '__main__':
    create_kerala_freelancers()
