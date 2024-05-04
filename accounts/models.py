from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.apps import apps


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email

User = get_user_model()


class Favourite(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    car = models.ForeignKey('booking.Car', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        CustomUser = apps.get_model('accounts', 'CustomUser')
        Car = apps.get_model('booking', 'Car')
        user = CustomUser.objects.get(id=self.user_id)
        car = Car.objects.get(id=self.car_id)
        return f'{user.email} - {car.name}'

class IDVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_image = models.ImageField(upload_to='id_images/')
    name = models.CharField(max_length=255, default='John Doe')
    dob = models.DateField(default=timezone.now)
    address = models.TextField(default='123 Main St')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if self.pk:  # if the object already exists in the database
            try:
                old_status = IDVerification.objects.get(pk=self.pk).status
            except IDVerification.DoesNotExist:
                old_status = None

            if old_status != 'rejected' and self.status == 'rejected':
                send_mail(
                    'Your ID verification was rejected',
                    'Your ID was rejected. Please upload a new one.',
                    'staff@vroom.com',
                    [self.user.email],
                    fail_silently=False,
                )
                self.delete()  # delete the instance
            elif old_status != 'verified' and self.status == 'verified':
                send_mail(
                    'Your ID verification was successful',
                    'Your ID has been successfully verified.',
                    'staff@vroom.com',
                    [self.user.email],
                    fail_silently=False,
                )
                super().save(*args, **kwargs)
            else:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        
    def __str__(self):
        return f'ID Verification for {self.name}'