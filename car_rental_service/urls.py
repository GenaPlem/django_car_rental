"""
URL configuration for car_rental_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from car_rental.views import (
    HomeView,
    CarsListView,
    CarDetailsView,
    ProfileView,
    BookingEditView,
    BookingDeleteView,
    PrivacyPolicyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('cars/', CarsListView.as_view(), name='cars-list'),
    path('cars/<int:pk>/', CarDetailsView.as_view(), name='car-details'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('booking/<int:pk>/edit/', BookingEditView.as_view(), name='booking_edit'),
    path('booking/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
    path('privacy-policy', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('accounts/', include('allauth.urls')),
]
