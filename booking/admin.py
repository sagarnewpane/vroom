from django.contrib import admin
from .models import Car
from .models import Booking

from django.utils.html import format_html

from django.contrib import admin
from django.db.models import Sum
from django.urls import path
from django.shortcuts import render
from .models import Car, Booking
from django.db.models import Avg
from django.urls import path
from django.http import HttpResponse
import csv

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'availability', 'hourly_rate', 'display_image']
    search_fields = [ 'model','availability', 'hourly_rate']

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url) if obj.image else None

    display_image.short_description = 'Image'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('revenue_report/', self.admin_site.admin_view(self.revenue_report), name='revenue_report'),
            path('revenue_report/<str:order>/', self.admin_site.admin_view(self.revenue_report), name='revenue_report_order'),
            path('export_revenue_report/', self.admin_site.admin_view(self.export_revenue_report), name='export_revenue_report'),
        ]
        return custom_urls + urls

    def export_revenue_report(self, request):
        cars = Car.objects.all()
        for car in cars:
            bookings = Booking.objects.filter(car=car, status='accepted')
            car.revenue = bookings.aggregate(Sum('estimated_price'))['estimated_price__sum'] or 0
            car.num_bookings = bookings.count()
            total_duration = sum((booking.drop_off_date - booking.pick_up_date).total_seconds() / 3600 for booking in bookings)
            car.avg_booking_duration = total_duration / car.num_bookings if car.num_bookings else 0
        cars = sorted(cars, key=lambda car: car.revenue, reverse=True)
        for i, car in enumerate(cars, start=1):
            car.rank = i

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="revenue_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Rank', 'Car Model', 'Availability', 'Hourly Rate', 'Number of Bookings', 'Average Booking Duration (hours)', 'Revenue'])
        for car in cars:
            writer.writerow([car.rank, car.model, car.availability, car.hourly_rate, car.num_bookings, car.avg_booking_duration, car.revenue])

        return response

    def revenue_report(self, request, order='desc'):
        cars = Car.objects.all()
        for car in cars:
            bookings = Booking.objects.filter(car=car, status='accepted')
            car.revenue = bookings.aggregate(Sum('estimated_price'))['estimated_price__sum'] or 0
            car.num_bookings = bookings.count()
            total_duration = sum((booking.drop_off_date - booking.pick_up_date).total_seconds() / 3600 for booking in bookings)
            car.avg_booking_duration = total_duration / car.num_bookings if car.num_bookings else 0
        cars = sorted(cars, key=lambda car: car.revenue, reverse=(order=='desc'))
        for i, car in enumerate(cars, start=1):
            car.rank = i
        return render(request, 'admin/revenue_report.html', {'cars': cars})

admin.site.unregister(Car)
admin.site.register(Car, CarAdmin)

class BookingStatusFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'pending':
            return queryset.filter(status='pending')
        elif self.value() == 'accepted':
            return queryset.filter(status='accepted')
        elif self.value() == 'rejected':
            return queryset.filter(status='rejected')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'booking_date', 'status')
    list_editable = ('status',)
    list_filter = (BookingStatusFilter,)
    base_site_template = 'admin/base_site.html'
    readonly_fields = ('user', 'car','pick_up_date', 'drop_off_date','estimated_price', 'booking_date',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['new_booking_requests'] = Booking.objects.filter(status='pending').count()
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if obj.status == 'accepted':
            obj.car.availability = 'unavailable'
            obj.car.save()
        super().save_model(request, obj, form, change)