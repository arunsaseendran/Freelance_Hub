from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booking_date', 'booking_time', 'customer_notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'customer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 
                                                    'placeholder': 'Any special instructions...'}),
        }
    
    def clean_booking_date(self):
        booking_date = self.cleaned_data.get('booking_date')
        if booking_date and booking_date < timezone.now().date():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return booking_date
    
    def clean(self):
        cleaned_data = super().clean()
        booking_date = cleaned_data.get('booking_date')
        booking_time = cleaned_data.get('booking_time')
        
        if booking_date and booking_time:
            booking_datetime = timezone.make_aware(
                timezone.datetime.combine(booking_date, booking_time)
            )
            if booking_datetime < timezone.now():
                raise forms.ValidationError("Booking time cannot be in the past.")
        
        return cleaned_data


class FreelancerNotesForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['freelancer_notes']
        widgets = {
            'freelancer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
