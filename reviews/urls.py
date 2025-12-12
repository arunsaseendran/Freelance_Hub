from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:booking_id>/', views.create_review, name='create_review'),
    path('<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('<int:review_id>/respond/', views.respond_to_review, name='respond_to_review'),
    path('freelancer/<int:freelancer_id>/', views.freelancer_reviews, name='freelancer_reviews'),
]
