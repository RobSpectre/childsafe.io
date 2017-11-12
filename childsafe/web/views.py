from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm

def index(request):
    return render(request, 'web/home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.phone_number = form.cleaned_data.get('phone_number')
            user.email = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.save()
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'web/signup.html',  {'form': form})

def login_page(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get("username", ""), password=request.POST.get("password", ""))
        login(request, user)
        if user is not None:
            return redirect('profile')
    return render(request, 'web/login.html')

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'web/profile.html')

def documentation(request):
    return render(request, 'web/documentation.html')
