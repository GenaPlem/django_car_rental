from django import forms
from .models import Booking
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
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if not re.match(r'^[a-zA-Zа-яА-Я\s]+$', surname):
            raise forms.ValidationError("Surname should only contain letters.")
        return surname

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

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
