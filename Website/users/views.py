from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("home") 
        else:
            return render(request, "users/login.html", {
            "message":"Wrong username or password!",
        })

    return render(request, "users/login.html")

def forgetPassword(request):
    return render(request, "users/forgetpassword.html")

def register(request):
    return render(request, "users/register.html")

def home(request):
    return render(request, 'users/home.html')

def product(request, product_label):
    return render(request, 'users/product.html', {
        "product_label":product_label
    })
