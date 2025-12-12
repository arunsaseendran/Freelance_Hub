# Freelancer Service Booking Platform

A Django-based marketplace that connects customers with verified freelancers for a wide range of services, complete with bookings, payments, and reviews.

## Features
- Role-based user accounts for admins, customers, and freelancers with verification workflows and profile management.@accounts/models.py#8-78
- Rich service catalog with categories, subcategories, and advanced search filters to help customers discover offerings quickly.@services/views.py#8-58
- Integrated booking flow with configurable cancellation windows and support for Razorpay, cash, and Google Pay payment options.@freelancer_platform/settings.py#164-188
- Ratings and review system to highlight top-performing freelancers and maintain quality.@accounts/models.py#34-66
- Email OTP verification backed by SMTP configuration for secure account onboarding.@accounts/models.py#77-119

## Tech Stack
- Python 3.x
- Django 4.2
- SQLite (default development database)
- Razorpay Python SDK for online payments

## Getting Started
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000/ in your browser to explore the app.

## Environment Configuration
1. Copy `.env.template` to `.env` and update the values for email credentials, Django secret key, and other environment-specific settings.@.env.template#1-14
2. Ensure the Razorpay API keys in `freelancer_platform/settings.py` are replaced with your own test or production credentials before deploying.@freelancer_platform/settings.py#166-188

## Project Structure
```
freelancer_platform/    # Global Django settings and URL routing
accounts/               # Custom user model, profiles, OTP verification
services/               # Service listings, categories, and search views
bookings/               # Booking management and scheduling logic
payments/               # Payment configuration and Razorpay integration
reviews/                # Feedback, ratings, and reputation tracking
templates/              # HTML templates including the home landing page
```

## Helpful Scripts
- `QUICKSTART.bat` / `QUICKSTART.txt`: Guided setup steps for Windows hosts.
- `setup_project.py`: Utility script to initialize environment variables and dependencies.
