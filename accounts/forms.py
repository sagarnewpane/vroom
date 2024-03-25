from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

from django.conf import settings

class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email','username','password1','password2')