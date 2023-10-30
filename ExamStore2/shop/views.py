from django.shortcuts import render, HttpResponse
from .models import Product
from django.shortcuts import render
from .forms import OrderForm

def index(request):
    all_products = Product.objects.all()
    return render(request , "index.html", {"products": all_products})


def chart(requset):
    return render(requset, "chart.html")


def order_view(request):
    form = OrderForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        order_count = form.cleaned_data['order_count']
        order_count += 1
        form.cleaned_data['order_count'] = order_count
    
    return render(request, 'ordeق.html', {'form': form})