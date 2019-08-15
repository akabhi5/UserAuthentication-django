from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .forms import SignUpForm, EditProfileForm

def home(request):
    return render(request, 'authenticate/home.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('you have been logged in'))
            return redirect('home')
        else:
            messages.success(request, ('error logging in. try again'))
            return redirect('login')

    return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('you have been logged out'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username'] # this is same as request.POST['username'] here we are fetchin value from form object
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            messages.success(request, ('you have registered'))
            login(request, user)
            return redirect('home')
    else:
         form = SignUpForm()

    context = {'form': form}
    return render(request, 'authenticate/register.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user) # passes user info to form itself
        if form.is_valid():
            form.save()
            messages.success(request, ('you haev edited your profile'))
            return redirect('home')
    else:
         form = EditProfileForm(instance=request.user)

    context = {'form': form}

    return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user) # passes user info to form itself
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ('you have edited your password'))
            return redirect('home')
    else:
         form = PasswordChangeForm(user=request.user)

    context = {'form': form}

    return render(request, 'authenticate/change_password.html', context)
