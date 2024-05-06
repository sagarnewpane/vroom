from django.urls import path
from .views import available_cars, book_car,view_bookings,search_cars,cancel_booking,payment

urlpatterns = [
    path('available-cars/', available_cars, name='available_cars'),
    path('search-cars/', search_cars, name='search_cars'),
    path('bookings/<int:car_id>/', book_car, name='bookings'),
    path('view_bookings/', view_bookings, name='view_bookings'),
    path('cancel_booking/', cancel_booking, name='cancel_booking'),
    path('payment/<int:car_id>/<str:pickup_datetime>/<str:dropoff_datetime>/<str:total_price>/', payment, name='payment'),

    # Add other URLs here if needed
]
