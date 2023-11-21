from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # to only authenticated users can fill the form
from .models import Car, Booking
from .forms import BookingForm
from .utils import calculate_total_price
from datetime import timedelta


class HomeView(TemplateView):
    template_name = 'index.html'


class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    paginate_by = 6


class CarDetailsView(DetailView, FormMixin):
    model = Car
    template_name = 'car_details.html'
    form_class = BookingForm

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()

        bookings = Booking.objects.filter(car=car)
        booked_dates = []

        for booking in bookings:
            current_date = booking.start_date
            while current_date <= booking.end_date:
                booked_dates.append(current_date.strftime("%m/%d/%Y"))
                current_date += timedelta(days=1)

        context['booked_dates'] = booked_dates

        if 'form' not in context:
            context['form'] = self.get_form()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.car = self.object

        booking.total_price = calculate_total_price(
            booking.start_date,
            booking.end_date,
            booking.car.price_per_day,
            booking.child_seat,
            booking.insurance_type
        )

        booking.save()
        return super(CarDetailsView, self).form_valid(form)
