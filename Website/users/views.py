from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from .models import Kurta, CartItem
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
    if request.user.is_authenticated:
        return render(request, 'users/home.html', context={
            "Kurtas":Kurta.objects.all(),
            "userName":request.user.username
            })
    return render(request, 'users/home.html', context={
        "Kurtas":Kurta.objects.all(),
    })
    

def product(request, product_label):
    try:
        kurta = Kurta.objects.get(name=product_label)
        return render(request, 'users/product.html', {
            "kurta":kurta,
        })
    except Kurta.DoesNotExist:
        # Handle the case where no Kurta with the specified name is found
        return render(request, "users/NotFound.html")
@login_required
def Cart(request, username):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user__username=username)
    
        kurta_list = [cart_item.kurta for cart_item in cart_items]
        return render(request,"users/addToCart.html", {
            "kurtas":kurta_list,
        })
    
    else:
        return render(request,"users/login.html", {
            "message":"Please Login to Add to Cart"
            })
def logout_view(request):
    logout(request)
    return redirect('home')