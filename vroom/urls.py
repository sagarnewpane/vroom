"""
URL configuration for vroom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from accounts import views as auth_view
from . import views
from django.contrib.auth import views as pass_view
from django.conf.urls.static import static
from django.conf import settings
from .views import CustomPasswordResetView

from booking.views import contact
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', auth_view.signup, name='signup'),
    path('login/', auth_view.login_view, name='login'),
    path('logout/', auth_view.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    # path('password-reset/', 
    #      pass_view.PasswordResetView.as_view(template_name = 'resetpass.html'), 
    #      name='password_reset'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', 
         pass_view.PasswordResetDoneView.as_view(template_name = 'resetpass_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         pass_view.PasswordResetConfirmView.as_view(template_name = 'resetpass_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         pass_view.PasswordResetCompleteView.as_view(template_name = 'resetpass_done_complete.html'), 
         name='password_reset_complete'),

    path('cars/', include('booking.urls')),
    path('account/', include('accounts.urls')),
    
    path('search/', views.search, name='search'),
    path('contact/', contact, name='contact'),

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
