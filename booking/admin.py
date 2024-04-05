from django.contrib import admin
from .models import Car
from .models import Booking

from django.utils.html import format_html

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'availability', 'num_seats', 'hourly_rate', 'display_image']
    search_fields = ['make', 'model','availability','num_seats', 'hourly_rate']

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url) if obj.image else None

    display_image.short_description = 'Image'


# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('user', 'car', 'booking_date', 'status')

# admin.site.register(Booking, BookingAdmin)
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'booking_date', 'status')

    def save_model(self, request, obj, form, change):
        if obj.status == 'accepted':
            obj.car.availability = 'unavailable'
            obj.car.save()
        super().save_model(request, obj, form, change)
