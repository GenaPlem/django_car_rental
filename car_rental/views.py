from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Car, Booking


# class CarList(generic.ListView):
#     model = Car
#     queryset = Car.objects.all()
#     template_name = ''
#     paginate_by = 9


def home(request):
    return render(request, 'index.html')


class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
