from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from booking.models import Booking, Car
from booking.forms import CarSearchForm
from decimal import Decimal

from django.shortcuts import render, redirect

def home(request):
    if request.method == 'POST':
        form = CarSearchForm(request.POST)
        if form.is_valid():
            pickup_datetime = form.cleaned_data['pickup_datetime']
            dropoff_datetime = form.cleaned_data['dropoff_datetime']
            location = form.cleaned_data['location']

            # Query available cars within the specified date range and location
            available_cars = Car.objects.filter(
                # availability='available',
                car_location=location
            )

            # Calculate duration in hours
            duration_hours = Decimal((dropoff_datetime - pickup_datetime).total_seconds()) / Decimal(3600)

            # Calculate price for each car
            for car in available_cars:
                car.total_price = round(duration_hours * car.hourly_rate, 2)
                
            return render(request, 'available_cars.html', {'cars': available_cars})
    else:
        form = CarSearchForm()

    return render(request, 'Vroom.html', {'form': form})