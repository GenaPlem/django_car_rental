from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from car_rental.models import Car, Booking
from car_rental.forms import BookingForm
from car_rental.utils import calculate_total_price
from datetime import timedelta


class HomeView(TemplateView):
    """
    View for home page
    """
    template_name = "index.html"


class CarsListView(ListView):
    """
    View for Our Cars page
    """
    model = Car
    template_name = "cars.html"
    context_object_name = "cars"
    paginate_by = 6

    # cars filter by available prop
    def get_queryset(self):
        return Car.objects.filter(available=True)


class CarDetailsView(DetailView, FormMixin):
    """
    View for Car reservation page with form to book it thats why I mixed DetailView and FormMixin
    """
    model = Car
    template_name = "car_details.html"
    form_class = BookingForm

    # if form fill out correctly
    def get_success_url(self):
        return reverse_lazy("profile")

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        kwargs["car"] = self.get_object()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.get_object()

        if "form" not in context:
            context["form"] = BookingForm(car=car)

        # already booked dates
        bookings = Booking.objects.filter(car=car)
        booked_dates = []

        for booking in bookings:
            current_date = booking.start_date
            while current_date <= booking.end_date:
                booked_dates.append(current_date.strftime("%Y-%m-%d"))
                current_date += timedelta(days=1)

        context["booked_dates"] = booked_dates

        return context

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        form = BookingForm(request.POST, car=car)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.car = self.get_object()

        # To get total price into db
        booking.total_price = calculate_total_price(
            booking.start_date,
            booking.end_date,
            booking.car.price_per_day,
            booking.child_seat,
            booking.insurance_type,
        )

        booking.save()
        messages.success(self.request, "Booking was successfully created!")
        return super(CarDetailsView, self).form_valid(form)

    # Incorrect form fill out
    def form_invalid(self, form):
        self.object = self.get_object()
        messages.error(self.request, "Something wrong with your booking!")
        return self.render_to_response(self.get_context_data(form=form))


class ProfileView(LoginRequiredMixin, ListView):
    """
    View for User Profile with list of all his bookings
    """
    model = Booking
    template_name = "profile.html"
    context_object_name = "bookings"

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by(
            "start_date"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class BookingEditView(LoginRequiredMixin, UpdateView):
    """
    View to edit booking
    """
    model = Booking
    form_class = BookingForm
    template_name = "booking_edit.html"

    def get_success_url(self):
        return reverse_lazy("profile")

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super(BookingEditView, self).get_form_kwargs()
        booking = self.get_object()
        kwargs["car"] = booking.car
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(BookingEditView, self).get_context_data(**kwargs)
        booking = self.get_object()
        car = booking.car

        other_bookings = Booking.objects.filter(car=car).exclude(
            id=booking.id
        )
        booked_dates = []
        for other_booking in other_bookings:
            current_date = other_booking.start_date
            while current_date <= other_booking.end_date:
                booked_dates.append(current_date.strftime("%Y-%m-%d"))
                current_date += timedelta(days=1)

        context["booked_dates"] = booked_dates
        context["car"] = car
        return context

    def dispatch(self, request, *args, **kwargs):
        """
        It checks if the user is authenticated,
        ensuring that only logged-in users can access the edit booking page.
        Additionally, it checks whether the booking has already been completed;
        if so, it redirects the user to the profile page with an error message,
        preventing any edits to past bookings.
        """
        if not request.user.is_authenticated:
            return redirect("profile")
        booking = self.get_object()
        if booking.is_completed():
            messages.error(
                request,
                "This booking has already expired and cannot be edited.",
            )
            return redirect("profile")
        return super(BookingEditView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(BookingEditView, self).form_valid(form)
        booking = form.save(commit=False)

        booking.total_price = calculate_total_price(
            booking.start_date,
            booking.end_date,
            booking.car.price_per_day,
            booking.child_seat,
            booking.insurance_type,
        )

        booking.save()
        messages.success(self.request, "Booking was successfully edited!")
        return response

    def form_invalid(self, form):
        self.object = self.get_object()
        messages.error(self.request, "Something wrong with your booking!")
        return self.render_to_response(self.get_context_data(form=form))


class BookingDeleteView(DeleteView):
    model = Booking
    success_url = reverse_lazy("booking_list")
    template_name = "booking_confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Booking was successfully canceled!")
        return reverse_lazy("profile")

    def dispatch(self, request, *args, **kwargs):
        """
        It checks if the user is authenticated,
        ensuring that only logged-in users can access the edit booking page.
        Additionally, it checks whether the booking has already been completed;
        if so, it redirects the user to the profile page with an error message,
        preventing any edits to past bookings.
        """
        if not request.user.is_authenticated:
            return redirect("profile")
        booking = self.get_object()
        if booking.is_completed():
            messages.error(
                request,
                "This booking has already expired and cannot be deleted.",
            )
            return redirect("profile")
        return super(BookingDeleteView, self).dispatch(
            request, *args, **kwargs
        )


class PrivacyPolicyView(TemplateView):
    template_name = "privacy_policy.html"
