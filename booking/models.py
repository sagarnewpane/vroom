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
    
    def calculate_revenue(self):
        bookings = Booking.objects.filter(car=self, status='accepted')
        total_revenue = bookings.aggregate(Sum('estimated_price'))['estimated_price__sum'] or 0
        return total_revenue

    @staticmethod
    def get_cars_by_revenue():
        cars = Car.objects.all()
        cars = sorted(cars, key=lambda car: car.calculate_revenue(), reverse=True)
        return cars

    @staticmethod
    def export_to_csv(cars, file_path):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Car Type', 'Car Model', 'Revenue']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for car in cars:
                writer.writerow({'Car Type': car.type, 'Car Model': car.model, 'Revenue': car.calculate_revenue()})


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('returned', 'Returned'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)  # Removed auto_now_add=True
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    drop_off_date = models.DateTimeField(default=datetime.now)
    pick_up_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Booking car {self.car.model} by {self.user.email}'
    

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='reviews', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(default=0)  # New rating field
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)