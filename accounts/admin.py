from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import IDVerification
from django.utils.html import format_html
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','username','password1','password2')
        }),
    )

    list_display = ('email', 'username')
    # list_editable = ('is_verified',)

admin.site.register(CustomUser,CustomUserAdmin)


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