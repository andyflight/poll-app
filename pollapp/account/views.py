from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from account.forms import UserRegistrationForm


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            redirect_url = request.GET.get('next', 'home')
            return redirect(redirect_url)
        else:
            messages.error(request, "Username Or Password is incorrect!!",
                           extra_tags='alert alert-warning alert-dismissible fade show')

    return render(request, 'account/login.html')


def register(request):
    if request.method == "POST":
        check1 = False
        check2 = False
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2= form.cleaned_data['password2']

            if password1 != password2:
                check1 = True
                messages.error(request, 'Password doesn\'t matched',
                               extra_tags='alert alert-warning alert-dismissible fade show')
            if User.objects.filter(username=username).exists():
                check2 = True
                messages.error(request, 'Username already exists',
                               extra_tags='alert alert-warning alert-dismissible fade show')

            if any([check1, check2]):
                messages.error(
                    request, "Registration Failed", extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1)
                messages.success(
                    request, f'Thanks for registering {user.username}!',
                    extra_tags='alert alert-success alert-dismissible fade show')
                valid = authenticate(request, username=username, password=password1)
                if valid is not None:
                    login(request, valid)
                return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form':form})

def log_out(request):
    logout(request)
    return redirect('home')
