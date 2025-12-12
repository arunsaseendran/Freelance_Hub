from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:service_id>/', views.create_booking, name='create_booking'),
    path('<int:pk>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('<int:pk>/accept/', views.accept_booking, name='accept_booking'),
    path('<int:pk>/reject/', views.reject_booking, name='reject_booking'),
    path('<int:pk>/complete/', views.complete_booking, name='complete_booking'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
]
