from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm



def index(request):
    return render(request,'index.html')

def logout(request):
    dj_logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")
    
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                dj_login(request, user)
                messages.info(request,"You are now logged in as {username}")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request,"login.html",{"form":form})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "register.html", {"register_form": form})
