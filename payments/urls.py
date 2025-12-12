from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<int:booking_id>/', views.payment_page, name='payment_page'),
    path('confirm/<int:payment_id>/', views.confirm_payment, name='confirm_payment'),
    path('history/', views.payment_history, name='payment_history'),
]
