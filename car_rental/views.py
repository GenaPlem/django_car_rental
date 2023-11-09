from django.shortcuts import render
from django.views import generic
from .models import Car, Booking


# class CarList(generic.ListView):
#     model = Car
#     queryset = Car.objects.all()
#     template_name = ''
#     paginate_by = 9


def home(request):
    return render(request, 'index.html')
