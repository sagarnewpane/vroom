from django import forms
from .models import Review

class CarSearchForm(forms.Form):
    # pickup_datetime = forms.DateTimeField(label='Pickup Date and Time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    pickup_datetime = forms.DateTimeField(label='Pickup Date and Time')
    # dropoff_datetime = forms.DateTimeField(label='Drop-off Date and Time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    dropoff_datetime = forms.DateTimeField(label='Drop-off Date and Time')

    location = forms.ChoiceField(label='Location', choices=[('Kathmandu','Kathmandu'),('Pokhara','Pokhara')], widget=forms.Select)



class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=[(i, i) for i in range(1, 6)], widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = ['content', 'rating']