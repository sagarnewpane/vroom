from django.db import models
from accounts.models import CustomUser

class Car(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
        ('maintenance', 'Maintenance'),
        name = models.CharField(max_length=255)
    ]

    LOCATION_CHOICES = [('Kathmandu','Kathmandu'),('Pokhara','Pokhara')]

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    car_location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default='unknown')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    num_seats = models.IntegerField(default=5)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    # drop_off_date = models.DateTimeField()
    # pick_up_date = models.DateTimeField()  # Add this line for pick up date

    def __str__(self):
        return f"{self.make} {self.model}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()  # Removed auto_now_add=True
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='pending')