from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from datetime import date, timedelta
from django.conf import settings
from django.http import HttpResponse
from . import models
import razorpay


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
        if "fabrics" not in request.session:
            request.session["fabrics"]=[]
        request.session["fabrics"]=request.POST.getlist('fabric[]')
        fabrics=request.POST.getlist('fabric[]')
        if fabrics != []:                
            kurtas=kurtas.filter(fabric__in=fabrics)
        for ind in range(len(request.session["fabrics"])):
            request.session["fabrics"][ind]=int(request.session["fabrics"][ind])

        if "designs" not in request.session:
            request.session["designs"]=[]
        request.session["designs"]=request.POST.getlist('design[]')
        designs=request.POST.getlist('design[]')
        if designs != []:            
            kurtas=kurtas.filter(design__in=designs)
        for ind in range(len(request.session["designs"])):
            request.session["designs"][ind]=int(request.session["designs"][ind])

        if "colors" not in request.session:
            request.session["colors"]=[]
        request.session["colors"]=request.POST.getlist('color[]')
        colors=request.POST.getlist('color[]')
        if colors != []:
            kurtas=kurtas.filter(color__in=colors)
        for ind in range(len(request.session["colors"])):
            request.session["colors"][ind]=int(request.session["colors"][ind])

        if "occasions" not in request.session:
            request.session["occasions"]=[]
        request.session["occasions"]=request.POST.getlist('occ[]')
        Occasions=request.POST.getlist('occ[]')
        if Occasions != []:
            kurtas=kurtas.filter(Occasion__in=Occasions)
        for ind in range(len(request.session["occasions"])):
            request.session["occasions"][ind]=int(request.session["occasions"][ind])
        print(request.session['occasions'])
        return render(request, 'users/home.html', context={
            "Kurtas":kurtas,
            "userName":request.user.username,
            "fabrics":models.Fabric.objects.all(),
            "colors": models.Color.objects.all(),
            "Design":models.Design.objects.all(),
            "Occasion":models.festival.objects.all(),
            "fab_ses":request.session["fabrics"],
            "des_ses":request.session["designs"],
            "col_ses":request.session["colors"],
            "occ_ses":request.session["occasions"]

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
            if not request.user.is_authenticated:
                return redirect('login')
            action=request.POST.get("action")
            
            if action=="Add-to-Cart":  
                size=request.POST["size"] 
                quantity = int(request.POST.get('quantity'))
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
    kurtas=[]
    for cartItems in cartList:
        kurtas.append(cartItems.kurta)

    subtotal=0
    for items in cartList:
        subtotal+=items.quantity*items.kurta.price
    shipping_date, shipping_day=getDeliveryDate()
    total=subtotal+40
    
    if request.method=="POST":
        # if 

        name=request.POST["name"]
        email=request.POST["email"]
        address=request.POST["address"]
        city=request.POST["city"]
        state=request.POST["state"]
        zip_code=request.POST["zip_code"]
        phone=int(request.POST["phone"])
        order=models.Orders.objects.create(
            amount=total,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            shipping_date=shipping_date
        )
        order.save()
        for kurta in kurtas:
            order.kurtas.add(kurta)
        
        for cartItem in cartList:
            models.CartItem.delete(cartItem)
        client=razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment=client.order.create({'amount':int(total*100), 'currency':'INR'})
    
        client=razorpay.Client(auth=(settings.KEY, settings.SECRET))
        payment=client.order.create({
            'amount':int(total*100), 'currency':'INR'
        })
        print(payment)
        return render(request, "users/payment.html", {
            'payment':payment,
        })
    else:
        return render(request, "users/BuyNow.html", {
        "cart_list":cartList,
        "sub_total":subtotal,
        "sdate":shipping_date,
        "sday":shipping_day,
        "ship_price":40,
        "total":total,
        "message": "Please Enter all fields",
        })
def orders(request, username):
    return render(request, 'users/NotFound.html')

def success(request):
    payment_id=request.GET.get('order_id')
    return render(request, "users/success.html")