from django.db import models
from django.contrib.auth.models import User,AbstractUser, Group, Permission
from django.contrib.postgres.fields import JSONField

class festival(models.Model):
    Type=models.CharField(max_length=50)
    def __str__(self) -> str:
        return f"{self.Type}"
class Fabric(models.Model):
    material=models.CharField(max_length=20)
    def __str__(self) -> str:
        return f"{self.material}"

class Color(models.Model):
    colour=models.CharField(max_length=20)
    def __str__(self) -> str:
        return f"{self.colour}"

class Design(models.Model):
    Texture=models.CharField(max_length=20)
    def __str__(self) -> str:
        return f"{self.Texture}"

class Kurta(models.Model):
    name = models.CharField(max_length=100)  # Increased max_length for the name
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    main_image = models.ImageField(upload_to='kurta_images/', null=True)  # Specify upload path for imagesmaterial
    zoom = models.ImageField(upload_to='kurta_images/', null=True)  # Specify upload path for imagesmaterial
    back = models.ImageField(upload_to='kurta_images/', null=True)  # Specify upload path for imagesmaterial
    
    Occasion = models.ForeignKey(festival, on_delete=models.CASCADE, related_name="Fest")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color")
    fabric=models.ForeignKey(Fabric, on_delete=models.CASCADE) 
    design=models.ForeignKey(Design, on_delete=models.CASCADE, related_name="design")
     
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation date/time
    updated_at = models.DateTimeField(auto_now=True)  # Track last update date/time

    s=models.IntegerField(default=1) # stock of respective size
    m=models.IntegerField(default=1) # stock of respective size
    l=models.IntegerField(default=1) # stock of respective size
    xl=models.IntegerField(default=1) # stock of respective size
    def reduce_size(self, size, quantity):
        match size:
            case 's':
                if self.s>=quantity:
                    self.s-=quantity
                    print(self.s)
                else: return False
            case 'm':
                if self.m >=quantity:
                    self.m-=quantity
                else: return False
            case 'l':
                if self.l>=quantity:
                    self.l-=quantity
                else: return False
            case 'xl':
                if self.xl >=quantity:
                    self.xl-=quantity
                else: return False
            
        return True
    def get_size(self, size):
        match size:
            case 's':
                return self.s
            case 'm':
                return self.m
            case 'l':
                return self.l            
            case 'xl':
                return self.xl
            

    def __str__(self):
        return f"{self.name} - {self.color} - ${self.price}"

    class Meta:
        verbose_name_plural = "Kurtas"
class CustomUser(AbstractUser):
    phone_no=models.CharField(max_length=12, null=True)
    wishList=models.ManyToManyField(Kurta, null=True)

class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="users")
    kurta = models.ForeignKey(Kurta, on_delete=models.CASCADE, related_name="kurta")
    size=models.CharField(default='s', max_length=3)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.user.username}'s Cart - {self.kurta.name}"
  
class Orders(models.Model):
    kurtas = models.ManyToManyField(Kurta)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone=models.CharField(max_length=111, default="")
    shipping_date=models.DateField(null=True)
    raz_order_id=models.CharField(max_length=100, null=True, blank=True)
    raz_payment_id=models.CharField(max_length=100, null=True, blank=True)
    raz_payment_sign=models.CharField(max_length=100, null=True, blank=True)

