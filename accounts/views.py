from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import IDVerification
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.shortcuts import get_object_or_404
from accounts.models import Favourite
from booking.models import Car
from django.core.files.base import ContentFile


# Create your views here.
from django.contrib import messages

def signup(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. You may now Login.')
            return redirect('login')
        else:
            messages.get_messages(request).used = True
    context = {"form": form}
    return render(request, 'signup.html', context)

def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                pass
            #     messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
            messages.get_messages(request).used = True

    context = {"form": form}
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')




from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import IDVerification

@login_required
def verify_id(request):
    try:
        id_verification = IDVerification.objects.get(user=request.user)
        if id_verification.status == 'verified':
            messages.error(request, 'Your ID has already been verified.')
            return render(request, 'verify_id.html')
        elif id_verification.status == 'pending':
            messages.error(request, 'Your ID is under verification. Please wait.')
            return render(request, 'verify_id.html')
    except IDVerification.DoesNotExist:
        pass

    if request.method == 'POST':
        id_image = request.FILES.get('id_photo')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        address = request.POST.get('address')

        if id_image and name and dob and address:
            validate_image = FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
            try:
                validate_image(id_image)
                sanitized_filename = id_image.name.replace(' ', '_')
                id_image.file = ContentFile(id_image.read(), name=sanitized_filename)
                dob = datetime.strptime(dob, '%Y-%m-%d 00:00').date()
                IDVerification.objects.create(user=request.user, id_image=id_image, name=name, dob=dob, address=address)
                messages.success(request, 'ID image and details uploaded successfully. They will be verified soon.')
            except ValidationError:
                messages.error(request, 'Invalid file type. Please upload a jpg, jpeg, or png image.')
        else:
            messages.error(request, 'Please fill in all fields and upload an image.')
    return render(request, 'verify_id.html')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favourite
from booking.models import Car

@login_required(login_url='login')
def toggle_favourite(request):
    car_id = request.POST.get('car_id')
    car = get_object_or_404(Car, id=car_id)
    favourited = False

    if Favourite.objects.filter(user=request.user, car=car).exists():
        Favourite.objects.filter(user=request.user, car=car).delete()
        favourited = False
    else:
        Favourite.objects.create(user=request.user, car=car)
        favourited = True

    print(favourited)

    return JsonResponse({'favourited': favourited})


@login_required(login_url='login')
def favourite_cars(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'favourites.html', {'favourites': favourites})

@login_required(login_url='login')
def check_favourite(request):
    car_id = request.POST.get('car_id')
    favourited = Favourite.objects.filter(user=request.user, car_id=car_id).exists()
    return JsonResponse({'favourited': favourited})