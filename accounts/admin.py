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
    list_display = ('user', 'status', 'id_image')
    list_editable = ('status',)
    list_filter = ('status',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['new_verification_requests'] = IDVerification.objects.filter(status='pending').count()
        return super().changelist_view(request, extra_context=extra_context)