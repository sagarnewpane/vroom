from django.shortcuts import render
from .forms import CarSearchForm
from .models import Car
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages framework
from django.shortcuts import redirect
from .models import Booking, Car

def search_cars(request):
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

def available_cars(request):
    # Retrieve all cars
    all_cars = Car.objects.all()

    return render(request, 'availablecar.html', {'cars': all_cars})





@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # Check if the user has already booked this car
    if Booking.objects.filter(user=request.user, car=car).exists():
        # If the user has already booked this car, display a message on the same page
        return render(request, 'booking.html', {'car': car, 'message': 'You have already booked this car.'})
    
    if request.method == 'POST':
        form = CarSearchForm(request.POST)
        if form.is_valid():
            pickup_datetime = form.cleaned_data['pickup_datetime']
            # dropoff_datetime = form.cleaned_data['dropoff_datetime']
            # location = form.cleaned_data['location'] # No need for location as it is used only for searching
            Booking.objects.create(user=request.user, car=car, status='pending',booking_date=pickup_datetime)
            return redirect('view_bookings')
        
    else:
        form = CarSearchForm()
    return render(request, 'booking.html', {'car': car,'form':form})

@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'view_bookings.html', {'bookings': bookings})

