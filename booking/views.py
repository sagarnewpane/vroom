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

from accounts.models import IDVerification
from accounts.models import Favourite


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

    car_location = request.GET.getlist('car_location')
    type = request.GET.getlist('type')
    availability = request.GET.getlist('availability')
    query = request.GET.get('q', '')  # Use an empty string as the default value

    print(car_location)

    # if request.GET:
    if 'q' in request.GET:  # Add this line to apply the search query filter
        cars = cars.filter(model__icontains=query)
    if 'car_location' in request.GET:
        cars = cars.filter(car_location__in=car_location)
    if 'type' in request.GET:
        cars = cars.filter(type__in=type)
    if 'availability' in request.GET:
        cars = cars.filter(availability__in=availability)
        

    return render(request, 'availablecar.html', {
        'cars': cars,
        'car_location': car_location,
        'type': type,
        'availability': availability,
        'query': query, 
        # Pass other context variables as needed
    })

@login_required(login_url='login')
def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    # Check if the user is verified
    try:
        id_verification = IDVerification.objects.get(user=request.user)
        id_verification_status = id_verification.status == 'verified'
    except IDVerification.DoesNotExist:
        id_verification_status = False
    
    # Check if the user has already booked this car
    if Booking.objects.filter(user=request.user, car=car).exists():
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
    return render(request, 'booking.html', {'car': car,'form':form, 'id_verification_status': id_verification_status})

@login_required(login_url='login')
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    favourites = Favourite.objects.filter(user=request.user)
    try:
        id_verification = IDVerification.objects.get(user=request.user)
        id_verification_status = id_verification.status == 'verified'
    except IDVerification.DoesNotExist:
        id_verification_status = False
    return render(request, 'userprofile.html', {'bookings': bookings, 'user': request.user, 'id_verification_status': id_verification_status, 'favourites': favourites})


from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

@csrf_exempt
def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = Booking.objects.get(id=booking_id)

        # Check if the current time is more than 3 hours from the booking time
        if timezone.now() > booking.booking_date + timedelta(hours=3):
            # Deduct 20% from the payment
            booking.estimated_price *=  Decimal('0.8')

        else:
            booking.estimated_price = 0
        # Change the booking status to 'rejected'
        booking.status = 'cancelled'
        # Save the changes
        booking.save()

        return JsonResponse({'status':'ok'})
        
    else:
        return JsonResponse({'status':'error'})