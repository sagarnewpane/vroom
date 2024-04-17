from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
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


def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('home')