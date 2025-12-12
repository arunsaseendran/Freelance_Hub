from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    path('my-services/', views.my_services, name='my_services'),
    path('create/', views.service_create, name='service_create'),
    path('<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_services, name='category_services'),
]
