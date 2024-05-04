from django.urls import path
from . import views

urlpatterns = [
    path('verify',views.verify_id,name='verify'),
    path('toggle_favourite/', views.toggle_favourite, name='toggle_favourite'),
    path('favourite_cars/', views.favourite_cars, name='favourite_cars'),
    path('check_favourite/', views.check_favourite, name='check_favourite'),
]
