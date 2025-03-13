
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegisterForm
from users.models import CustomUser
# Create your views here.

def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:index')
                else:
                    messages.error(request, 'Disabled account')
            else:
                messages.error(request, 'Invalid email or password')

    return render(request, 'users/login.html', {'form': form})


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = CustomUser.objects.create(
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['name'],
                password=form.cleaned_data['password'],
            )
            user.save()
            messages.success(request, 'Registration successful. Please login.')
            return redirect('users:login_page')

    return render(request, 'users/register.html', {'form': form})


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('shop:index')