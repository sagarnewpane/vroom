from django.db import models
from accounts.models import CustomUser
from datetime import datetime

class Car(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('maintenance', 'Maintenance'),
    ]

    LOCATION_CHOICES = [('Kathmandu','Kathmandu'),('Pokhara','Pokhara')]
    TYPES = [('Sedan','Sedan'),('Sports','Sports'),('SUV','SUV'),('EV','EV'),('MPV','MPV')]

    car_location = models.CharField(max_length=100, choices=LOCATION_CHOICES)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    type = models.CharField(max_length=20, choices=TYPES, default='Unknown')
    model = models.CharField(max_length=100)
    mileage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    transmission = models.CharField(max_length=50)
    seats = models.IntegerField(default=0)
    luggage = models.IntegerField(default=0)
    fuel = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.type} {self.model}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)  # Removed auto_now_add=True
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    drop_off_date = models.DateTimeField(default=datetime.now)
    pick_up_date = models.DateTimeField(default=datetime.now)