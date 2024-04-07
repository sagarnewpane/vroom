from django import forms
from .models import Booking

class CarSearchForm(forms.Form):
    # pickup_datetime = forms.DateTimeField(label='Pickup Date and Time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    pickup_datetime = forms.DateTimeField(label='Pickup Date and Time')
    # dropoff_datetime = forms.DateTimeField(label='Drop-off Date and Time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    dropoff_datetime = forms.DateTimeField(label='Drop-off Date and Time')

    location = forms.ChoiceField(label='Location', choices=[('Kathmandu','Kathmandu'),('Pokhara','Pokhara')], widget=forms.Select)