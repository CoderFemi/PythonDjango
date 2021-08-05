from django.contrib import auth
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import RegisterForm


def register_user(request):
    page = 'register'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Get user object and make changes before saving
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('profiles')
        else:
            messages.error(request, 'An error occurred.')
    else:
        form = RegisterForm()
    
    context = {'page': page, 'form': form}
    return render(request, 'users/auth.html', context)


def login_user(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('profiles')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'users/auth.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'Goodbye!')
    return redirect('/')


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)


def show_profile(request, param):
    profile = Profile.objects.get(id=param)
    context = {'profile': profile}
    return render(request, 'users/show_profile.html', context)