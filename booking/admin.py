from django.contrib import admin
from .models import Car
from .models import Booking

from django.utils.html import format_html

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['model', 'availability', 'hourly_rate', 'display_image']
    search_fields = [ 'model','availability', 'hourly_rate']

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url) if obj.image else None

    display_image.short_description = 'Image'


# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('user', 'car', 'booking_date', 'status')

# admin.site.register(Booking, BookingAdmin)


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

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['new_booking_requests'] = Booking.objects.filter(status='pending').count()
        return super().changelist_view(request, extra_context=extra_context)

    def save_model(self, request, obj, form, change):
        if obj.status == 'accepted':
            obj.car.availability = 'unavailable'
            obj.car.save()
        super().save_model(request, obj, form, change)