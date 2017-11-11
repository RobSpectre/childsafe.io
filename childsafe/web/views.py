from django.shortcuts import render

def index(request):
    return render(request, 'web/home.html')

def signup(request):
    return render(request, 'web/signup.html')

def login(request):
    return render(request, 'web/login.html')

def profile(request):
    return render(request, 'web/profile.html')

def documentation(request):
    return render(request, 'web/documentation.html')
