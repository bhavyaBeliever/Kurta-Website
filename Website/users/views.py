from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from datetime import date, timedelta

from django.urls import reverse
from . import models

def get_kurtas_by_fabric_ids(fabric_ids):
    queryset = models.Kurta.objects.all()
    if fabric_ids:
        queryset = queryset.filter(fabric_id__in=fabric_ids)
    kurtas = queryset.all()
    return kurtas
def get_kurtas_by_design_ids(design_ids):
    queryset = models.Kurta.objects.all()
    if design_ids:
        queryset = queryset.filter(design_id__in=design_ids)
    kurtas = queryset.all()
    return kurtas
def get_kurtas_by_color_ids(color_ids):
    queryset = models.Kurta.objects.all()
    if color_ids:
        queryset = queryset.filter(color_id__in=color_ids)
    kurtas = queryset.all()
    return kurtas
def get_kurtas_by_occasions_ids(occasions_ids):
    queryset = models.Kurta.objects.all()
    if occasions_ids:
        queryset = queryset.filter(occasions_id__in=occasions_ids)
    kurtas = queryset.all()
    return kurtas

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
    if request.method=='POST':
        kurtas=models.Kurta.objects.all()
        fabrics=request.POST.getlist('fabric[]')
        if fabrics != []:                
            kurtas=kurtas.filter(fabric__in=fabrics)
        designs=request.POST.getlist('design[]')
        if designs != []:            
            kurtas=kurtas.filter(design__in=designs)
        colors=request.POST.getlist('color[]')
        if colors != []:
            kurtas=kurtas.filter(color__in=colors)
    
        Occasions=request.POST.getlist('occ[]')
        if Occasions != []:
            kurtas=kurtas.filter(Occasion__in=Occasions)
        return render(request, 'users/home.html', context={
            "Kurtas":kurtas,
            "userName":request.user.username,
            "fabrics":models.Fabric.objects.all(),
            "colors": models.Color.objects.all(),
            "Design":models.Design.objects.all(),
            "Occasion":models.festival.objects.all(),
        })

    else:
        kurtas=models.Kurta.objects.all()
        return render(request, 'users/home.html', context={
            "Kurtas":kurtas,
            "userName":request.user.username,
            "fabrics":models.Fabric.objects.all(),
            "colors": models.Color.objects.all(),
            "Design":models.Design.objects.all(),
            "Occasion":models.festival.objects.all(),
            })




def product(request, kurta_id):
    try:
        kurta = models.Kurta.objects.get(id=kurta_id)
        if request.method=='POST':
            quantity = int(request.POST.get('quantity'))
            if not request.user.is_authenticated:
                return redirect('login')
            action=request.POST.get("action")
            
            if action=="Add-to-Cart":  
                size=request.POST["size"] 
                print("Inside Post")
                if kurta.reduce_size(size=size, quantity=quantity):
                    print(kurta.id,kurta.s)
                    cart_item, created=models.CartItem.objects.get_or_create(user=request.user,kurta=kurta, size=size)
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
    except models.Kurta.DoesNotExist:
        # Handle the case where no Kurta with the specified name is found
        return render(request, "users/NotFound.html")
@login_required
def Cart(request, username):
    if request.method=='POST':
        if request.POST['remove']=='remove':
            kurta_id=int(request.POST['kurta_id'])
            kurta=models.Kurta.objects.get(pk=kurta_id)
            userProduct=models.CartItem.objects.get(kurta=kurta, user=request.user)
            models.CartItem.delete(userProduct)
            return redirect('Cart', username=request.user.username)
    if request.user.is_authenticated:
        cart_items = models.CartItem.objects.filter(user__username=username)
    
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
def getDeliveryDate():
    today = date.today()
    today_weekday = today.weekday()
    day_names = {0: "Monday",1: "Tuesday",2: "Wednesday",3: "Thursday",4: "Friday",5: "Saturday",6: "Sunday",}
    today_day = day_names[today_weekday]
    future_date = today + timedelta(days=4)
    future_weekday = future_date.weekday()
    future_day = day_names[future_weekday]

    return future_date, future_day

def BuyNow(request, username):
    cartList=models.CartItem.objects.filter(user=request.user)
    subtotal=0
    for items in cartList:
        subtotal+=items.quantity*items.kurta.price
    shipping_date, shipping_day=getDeliveryDate()
    return render(request, "users/BuyNow.html", {
        "cart_list":cartList,
        "sub_total":subtotal,
        "sdate":shipping_date,
        "sday":shipping_day,
        "ship_price":40,
        "total":40+subtotal,
    })