from django.db import models
from django.contrib.auth.models import User,AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    phone_no=models.CharField(max_length=12, null=True)
class festival(models.Model):
    Type=models.CharField(max_length=50)
    def __str__(self) -> str:
        return f"{self.Type}"


class Kurta(models.Model):
    Occasion = models.ForeignKey(festival, on_delete=models.CASCADE, related_name="Fest")
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    color = models.CharField(max_length=50)
    name = models.CharField(max_length=100)  # Increased max_length for the name
    image = models.ImageField(upload_to='kurta_images/')  # Specify upload path for images
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation date/time
    updated_at = models.DateTimeField(auto_now=True)  # Track last update date/time
    fabric=models.CharField(max_length=50)
    design=models.CharField(max_length=50)
    s=models.IntegerField(default=1)# stock of respective size
    m=models.IntegerField(default=1)# stock of respective size
    l=models.IntegerField(default=1)# stock of respective size
    xl=models.IntegerField(default=1)# stock of respective size
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

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kurta = models.ForeignKey(Kurta, on_delete=models.CASCADE)
    size=models.CharField(default='s', max_length=3)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.user.username}'s Cart - {self.kurta.name}"
  
