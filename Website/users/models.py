from django.db import models
from django.contrib.auth.models import User
# from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
# class User(models.Model):
#     mobileNo=PhoneNumberField()
class festival(models.Model):
    Type=models.CharField(max_length=50)
    def __str__(self) -> str:
        return f"{self.Type}"

class Kurta(models.Model):
    Occasion = models.ForeignKey(festival, on_delete=models.CASCADE, related_name="kurtas")
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for price to handle cents/dollars
    color = models.CharField(max_length=50)
    name = models.CharField(max_length=100)  # Increased max_length for the name
    image = models.ImageField(upload_to='kurta_images/')  # Specify upload path for images
    size = models.CharField(max_length=10, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')])  # Example sizes, you can adjust as needed
    stock = models.PositiveIntegerField(default=0)  # Track available stock
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation date/time
    updated_at = models.DateTimeField(auto_now=True)  # Track last update date/time
    fabric=models.CharField(max_length=50)
    design=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.color} - ${self.price} ({self.get_size_display()})"

    class Meta:
        verbose_name_plural = "Kurtas"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kurta = models.ForeignKey(Kurta, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username}'s Cart - {self.kurta.name}"
  
