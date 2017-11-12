from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import ChildsafeUser


def index(request):
    return render(request, 'web/home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.phone_number = form.cleaned_data.get('phone_number')
            user.email = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user.save()
            childsafeUser = ChildsafeUser.objects.create(user=user)
            childsafeUser.first_name = user.first_name
            childsafeUser.last_name = user.last_name
            childsafeUser.organization = form.cleaned_data.get('organization')
            childsafeUser.email_address = form.cleaned_data.get('username')
            childsafeUser.phone_number = form.cleaned_data.get('phone_number')
            childsafeUser.save()
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request,
                  'web/signup.html',
                  {'form': form})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get("username", ""),
                            password=request.POST.get("password", ""))
        login(request, user)
        if user is not None:
            return redirect('profile')
    return render(request, 'web/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='/login/')
def profile(request):
    user = request.user

    if request.method == 'POST':
        if request.POST.get("form") == "notifications":
            user.childsafeuser.sms_notifications = \
                request.POST.get("smsNotifications")
            user.childsafeuser.email_notifications = \
                request.POST.get("emailNotifications")
            user.childsafeuser.phone_notifications = \
                request.POST.get("phoneNotifications")
            user.save()
            user.refresh_from_db()
    context = {
        "user": user
    }
    return render(request, 'web/profile.html', context)


def documentation(request):
    return render(request, 'web/documentation.html')
