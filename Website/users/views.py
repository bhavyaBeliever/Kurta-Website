from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

from django.urls import reverse
from .models import Kurta, CartItem

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
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def home(request):
    
    return render(request, 'users/home.html', context={
            "Kurtas":Kurta.objects.all(),
            "userName":request.user.username
            })




def product(request, kurta_id):
    try:
        kurta = Kurta.objects.get(id=kurta_id)
        if request.method=='POST':
            quantity = int(request.POST.get('quantity'))
            if not request.user.is_authenticated:
                return redirect('login')
            action=request.POST.get("action")
            print(action)
            if action=="Add-to-Cart":  
                size=request.POST["size"] 
                print("Inside Post")
                if kurta.reduce_size(size=size, quantity=quantity):
                    print(kurta.id,kurta.s)
                    cart_item, created=CartItem.objects.get_or_create(user=request.user,kurta=kurta, size=size)
                    if not created:
                        cart_item.quantity+=quantity
                    else:
                        print(quantity)
                        cart_item.quantity=quantity
        
                    cart_item.save()
                    return redirect('Cart', username=request.user.username)
                else:
                    return render(request, 'users/product.html', {
                        "kurta":kurta,
                        "message":"Sorry Out of stock",
                    })
       
        return render(request, 'users/product.html', {
            "kurta":kurta,
        })
    except Kurta.DoesNotExist:
        # Handle the case where no Kurta with the specified name is found
        return render(request, "users/NotFound.html")
@login_required
def Cart(request, username):
    if request.method=='POST':
        if request.POST['remove']=='remove':
            kurta_id=int(request.POST['kurta_id'])
            kurta=Kurta.objects.get(pk=kurta_id)
            userProduct=CartItem.objects.get(kurta=kurta, user=request.user)
            CartItem.delete(userProduct)
            return redirect('Cart', username=request.user.username)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user__username=username)
    
        cartItems = [cart_item for cart_item in cart_items]
        return render(request,"users/ViewCart.html", {
            "cartView":cartItems,
        })
    
    else:
        return render(request,"users/login.html", {
            "message":"Please Login to Add to Cart"
            })
def logout_view(request):
    logout(request)
    return redirect('home')
def BuyNow(request, username):
    cartList=CartItem.objects.filter(user=request.user)
    return render(request, "users/BuyNow.html", {
        "cart_list":cartList,
    })