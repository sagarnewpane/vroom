from django.contrib import admin
from django.urls import path, include
from .views import available_cars, book_car, view_bookings, search_cars

urlpatterns = [
    path('admin/', admin.site.urls),
    path('available-cars/', available_cars, name='available_cars'),
    path('search-cars/', search_cars, name='search_cars'),
    path('bookings/<int:car_id>/', book_car, name='bookings'),
    path('view_bookings/', view_bookings, name='view_bookings'),
    path('book/', book_car, name='book_car'),
    path('', include('.urls')),
]
