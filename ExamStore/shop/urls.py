from django.urls import path, include
from django.urls import path
from shop import views
from .views import ProductsView, CartView

urlpatterns = [
    path('products/', views.ProductsView.as_view(), name="product"),
        path('cart/', views.CartView.as_view(), name="cart"),
]
