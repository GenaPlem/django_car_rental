from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('name', 'surname', 'start_date', 'end_date', 'child_seat', 'insurance_type', 'rules_agreement')
        widgets = {
            'start_date': forms.TextInput(attrs={'autocomplete': 'off'}),
            'end_date': forms.TextInput(attrs={'autocomplete': 'off'}),
            'rules_agreement': forms.CheckboxInput(attrs={'required': 'required'}),
        }
    
    def clean_rules_agreement(self):
        rules_agreement = self.cleaned_data.get('rules_agreement')
        if not rules_agreement:
            raise forms.ValidationError("You must agree to the rules to proceed.")
        return rules_agreement
        