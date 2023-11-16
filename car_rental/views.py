from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView
from .models import Car, Booking


class HomeView(TemplateView):
    template_name = 'index.html'


class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    paginate_by = 6


class CarDetailsView(DetailView):
    model = Car
    template_name = 'car_details.html'
