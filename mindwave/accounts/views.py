from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm, UserForm
from django.shortcuts import redirect
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        
        return redirect("/login/")
    else:
        form = RegisterForm()
    
    return render(request, "accounts/register.html", {"form": form})

import os

@login_required
def profile(request):
    path = 'static/img/avatars'
    img_list = os.listdir(path)

    context = {
        "profile": request.user.profile,
        'images': img_list,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')  # Redirect to a profile page or another page
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            return redirect('/')
    return render(request, 'registration/login.html')


@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')


def home(request):
    return redirect('/')

from .models import Profile

def setAvatar(request):
    img = request.POST['imgInfo']

    #SET AVATAR
    #TODO display it
    user = Profile.objects.get(user=request.user)
    user.profile_picture.name = f'{img}'
    user.save()
    return redirect('profile')