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
    list_filter = ('status',)  # add this line

    def display_id_image(self, obj):
        return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" /></a>', obj.id_image.url, obj.id_image.url)
    display_id_image.short_description = 'ID Image'