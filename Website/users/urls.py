from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("",views.home, name="home"),
    path("kurtas/<str:kurta_id>", views.product, name="product"),
    path("<str:username>/myCart", views.Cart, name="Cart"), 
    path("<str:username>/Buy-Now", views.BuyNow, name="BuyNow"),
    path("logout/", views.logout_view, name='logout'),
    path("<str:username>/myOrders", views.orders, name='myOrders'),
    path("success/", views.success, name='success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)