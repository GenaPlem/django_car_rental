from django import forms
from .models import Booking
from datetime import datetime, timedelta
import re


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.car = kwargs.pop('car', None)
        super(BookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = ('name', 'surname', 'start_date', 'end_date', 'child_seat', 'insurance_type', 'rules_agreement')
        widgets = {
            'start_date': forms.TextInput(attrs={'autocomplete': 'off'}),
            'end_date': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[a-zA-Zа-яА-Я\s]+$', name):
            raise forms.ValidationError("Name should only contain letters.")
        if len(name) < 3:
            raise forms.ValidationError("Name should be more than 2 symbols.")
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if not re.match(r'^[a-zA-Zа-яА-Я\s]+$', surname):
            raise forms.ValidationError("Surname should only contain letters.")
        if len(surname) < 3:
            raise forms.ValidationError("Surname should be more than 2 symbols.")
        return surname

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        today = datetime.today().date()

        if start_date:
            if start_date < today:
                self.add_error('start_date', 'The start date cannot be in the past.')

        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', 'The end date must be after the start date.')

        if end_date > start_date + timedelta(days=30):
            self.add_error('end_date', 'The booking cannot be longer than one month.')

        if start_date and end_date and self.car:
            overlapping_bookings = Booking.objects.filter(
                car=self.car,
                start_date__lte=end_date,
                end_date__gte=start_date
            ).exclude(pk=self.instance.pk).exists()

            if overlapping_bookings:
                self.add_error('end_date', 'This car is already booked for some of your selected dates.')

        return cleaned_data

    def clean_rules_agreement(self):
        rules_agreement = self.cleaned_data.get('rules_agreement')
        if not rules_agreement:
            raise forms.ValidationError("You must agree to the rules to proceed.")
        return rules_agreement
