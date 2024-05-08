from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from booking.models import Booking, Car
from booking.forms import CarSearchForm
from decimal import Decimal
from booking.models import Car
from django.db.models import Count

# Home Page
def home(request):
    if request.method == 'POST':
        form = CarSearchForm(request.POST)
        if form.is_valid():
            pickup_datetime = form.cleaned_data['pickup_datetime']
            dropoff_datetime = form.cleaned_data['dropoff_datetime']
            location = form.cleaned_data['location']

            # Query available cars within the specified date range and location
            available_cars = Car.objects.filter(
                availability='available',
                car_location=location
            )

            # Calculate duration in hours
            duration_hours = Decimal((dropoff_datetime - pickup_datetime).total_seconds()) / Decimal(3600)

            # Calculate price for each car
            for car in available_cars:
                car.total_price = round(duration_hours * car.hourly_rate, 2)
                
            return render(request, 'availablecar.html', {'cars': available_cars})
    else:
        form = CarSearchForm()
    
    # Sort 3 featured cars (most expensive)
    featured_cars = Car.objects.filter(
        availability='available'
    ).order_by('-hourly_rate')[:3]

    # Sort 3 popular cars (most booked)
    popular_cars = Car.objects.filter(
        availability='available'
    ).annotate(
        num_bookings=Count('booking')  # Use 'booking' to count the number of Booking instances for each Car
    ).order_by('-num_bookings')[:3]


    return render(request, 'Vroom.html', {'form': form,'featured_cars': featured_cars,'popular_cars': popular_cars})

def search(request):
    car_location = request.GET.getlist('car_location')
    type = request.GET.getlist('type')
    availability = request.GET.getlist('availability')

    query = request.GET.get('q', '')  # Use an empty string as the default value
    results = Car.objects.all()

    if query:
        results = results.filter(model__icontains=query)
        if results and car_location:
            results = results.filter(car_location__in=car_location)
        if results and type:
            results = results.filter(type__in=type)
        if results and availability:
            results = results.filter(availability__in=availability)

    return render(request, 'availablecar.html', {
        'cars': results, 
        'query': query, 
        'car_location': car_location,
        'type': type,
        'availability': availability,
    })

# About Page
def about(request):
    return render(request,'about.html')

# FAQ Page
def faq(request):
    return render(request,'faq.html')
