from django import forms
from .models import Booking

class CarSearchForm(forms.Form):
    pickup_datetime = forms.DateTimeField(label='Pickup Date and Time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    dropoff_datetime = forms.DateTimeField(label='Drop-off Date and Time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    location = forms.ChoiceField(label='Location', choices=[('Kathmandu','Kathmandu'),('Pokhara','Pokhara')], widget=forms.Select)
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user_email', 'car_model', 'pickup_location', 'dropoff_location', 'pickup_date', 'dropoff_date']