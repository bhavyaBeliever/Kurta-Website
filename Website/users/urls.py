from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("",views.home, name="home"),
    path("kurtas/<str:product_label>", views.product, name="product_label")
       
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)