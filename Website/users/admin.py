from django.contrib import admin
from .models import Kurta, festival, CartItem, CustomUser

admin.site.register(festival)
admin.site.register(Kurta)
admin.site.register(CartItem)
admin.site.register(CustomUser)

