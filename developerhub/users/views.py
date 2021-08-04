from django.shortcuts import render
from .models import Profile

# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def show_profile(request, param):
    profile = Profile.objects.get(id=param)
    context = {'profile': profile}
    return render(request, 'users/show_profile.html', context)