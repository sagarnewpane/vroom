from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import IDVerification
from django.utils.html import format_html
from booking.models import Booking
from django.shortcuts import render
# Register your models here.

from django.urls import path
from django.http import HttpResponse
from django.db.models import Count, Sum
import csv

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username')
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','username','password1','password2')
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('user_report/', self.admin_site.admin_view(self.user_report), name='user_report'),
            path('user_report/<str:order>/', self.admin_site.admin_view(self.user_report), name='user_report_order'),
            path('export_user_report/', self.admin_site.admin_view(self.export_user_report), name='export_user_report'),
        ]
        return custom_urls + urls

    def user_report(self, request, order='desc'):
        users = CustomUser.objects.all()

        for user in users:
            bookings = Booking.objects.filter(user=user)
            user.total_spend = bookings.aggregate(Sum('estimated_price'))['estimated_price__sum'] or 0
            user.num_bookings = bookings.count()

        users = sorted(users, key=lambda user: user.total_spend, reverse=(order=='desc'))
        for i, user in enumerate(users, start=1):
            user.rank = i
        return render(request, 'admin/user_report.html', {'users': users})

    def export_user_report(self, request):
        users = CustomUser.objects.all()

        for user in users:
            bookings = Booking.objects.filter(user=user)
            user.total_spend = bookings.aggregate(Sum('estimated_price'))['estimated_price__sum'] or 0
            user.num_bookings = bookings.count()

        users = sorted(users, key=lambda user: user.total_spend, reverse=True)
        for i, user in enumerate(users, start=1):
            user.rank = i

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="user_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Rank', 'Email', 'Username', 'Number of Bookings', 'Total Spend'])
        for user in users:
            writer.writerow([user.rank, user.email, user.username, user.num_bookings, user.total_spend])

        return response
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(IDVerification)
class IDVerificationAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    search_fields = ('user__email', 'name')
    list_display = ['get_user_email','id_image','status']
    list_uneditable = ('get_user_email', 'id_image', 'name', 'dob', 'address')
    exclude = ('user',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.list_uneditable
        return []

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'User Email'  # Sets column header

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['new_verification_requests'] = IDVerification.objects.filter(status='pending').count()
        return super().changelist_view(request, extra_context=extra_context)