from django.shortcuts import render, HttpResponse
from .models import Product
from django.shortcuts import render
from django.views import View
from shop.models import Order

class ProductsView(View):
    def get(self, request):
        all_products = Product.objects.all()
        return render(request , "index.html", {"products": all_products})


class CartView(View):
    def get(self, request):
            basket = Order.get_basket(request.user)
            if basket:
                order_items = basket.orderitem_set.all()
                return render(request, "chart.html", {"basket": basket, "items": order_items, "full_price": basket.order_full_price})
