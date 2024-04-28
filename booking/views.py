from django.shortcuts import render
from .forms import CarSearchForm
from .models import Car
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages framework
from django.shortcuts import redirect
from .models import Booking, Car
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from vroom.settings import EMAIL_HOST_USER


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
    cars = Car.objects.all()

    if request.GET:
        if 'car_location' in request.GET:
            cars = cars.filter(car_location__in=request.GET.getlist('car_location'))
        if 'type' in request.GET:
            cars = cars.filter(type__in=request.GET.getlist('type'))
        if 'availability' in request.GET:
            cars = cars.filter(availability__in=request.GET.getlist('availability'))

    return render(request, 'availablecar.html', {'cars': cars})


@login_required(login_url='login')
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # Check if the user has already booked this car
    if Booking.objects.filter(user=request.user, car=car).exists():
        # If the user has already booked this car, display a message on the same page
        # return render(request, 'booking.html', {'car': car, 'message': {'You have already booked this car.','isbooked': True}})
        return render(request, 'booking.html', {'car': car, 'message': 'You have already booked this car.', 'isbooked': True})
    
    if request.method == 'POST':
        form = CarSearchForm(request.POST)
        if form.is_valid():
            pickup_datetime = form.cleaned_data['pickup_datetime']
            dropoff_datetime = form.cleaned_data['dropoff_datetime']

            duration_hours = Decimal((dropoff_datetime - pickup_datetime).total_seconds()) / Decimal(3600)
            total_price = round(duration_hours * car.hourly_rate, 2)

            # location = form.cleaned_data['location'] # No need for location as it is used only for searching
            Booking.objects.create(user=request.user, car=car, status='pending',estimated_price=total_price,drop_off_date=dropoff_datetime,pick_up_date=pickup_datetime)
            
            # Send an email to the user
            send_mail(
                f'Booking Successful for Car {car.model} on {pickup_datetime.date()}',
                f'''Your booking has been successful and waiting confiramation by the dealer.
                Car: {car.model}.
                For date {pickup_datetime.date()} to {dropoff_datetime.date()}.
                Total Price: {total_price}.\n
                Thank you for booking with us.
                ''',
                EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )

            return redirect('view_bookings')
        
    else:
        form = CarSearchForm()
    return render(request, 'booking.html', {'car': car,'form':form})


@login_required(login_url='login')
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'userprofile.html', {'bookings': bookings, 'user': request.user})

@csrf_exempt
def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        Booking.objects.filter(id=booking_id).delete()
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status':'error'})