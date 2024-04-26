from .models import Booking

def new_requests(request):
    return {'new_requests': Booking.objects.filter(status='pending').count()}