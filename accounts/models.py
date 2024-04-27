from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model




# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.email

User = get_user_model()

class IDVerification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_image = models.ImageField(upload_to='id_images/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        if self.pk:  # if the object already exists in the database
            old_status = IDVerification.objects.get(pk=self.pk).status
            if old_status != 'rejected' and self.status == 'rejected':
                send_mail(
                    'Your ID verification was rejected',
                    'Your ID was rejected. Please upload a new one.',
                    'from@example.com',
                    [self.user.email],
                    fail_silently=False,
                )
                self.delete()  # delete the instance
            else:
                super().save(*args, **kwargs)
