from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .views import *
from .forms import SignUpForm
# Create your views here.


def home(request):
    context = {
        'title': "Home"
    }
    return render(request, 'home.html', context)


@login_required(login_url='signin')
def index(request):
    context = {
        'title': "Index"
    }
    return render(request, 'index.html', context)


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username Or Password is incorrect')
    context = {
        'title': "SignIn"
    }
    return render(request, 'signin.html', context)


def signout(request):
    logout(request)
    messages.success(request, 'You Are Logged Out')
    return redirect('signin')


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(
                request, f"Account Created Successfully for {user} ")
            return redirect('signin')
    context = {
        'form': form,
        'title': "SignUp"
    }
    return render(request, 'signup.html', context)
