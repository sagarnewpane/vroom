from .models import Booking
from accounts.models import IDVerification

def new_requests(request):
    return {
        'new_booking_requests': Booking.objects.filter(status='pending').count(),
        'new_verification_requests': IDVerification.objects.filter(status='pending').count(),
    }