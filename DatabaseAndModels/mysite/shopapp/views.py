from django.http import HttpRequest
from django.shortcuts import render

from shopapp.models import Product, Order


# Create your views here.
def index(request:HttpRequest):
    context = {

    }
    return render(request, 'shopapp/index.html', context=context)

def product(request:HttpRequest):
    context = {
        "product_list": Product.objects.all()
    }
    return render(request, 'shopapp/product.html', context=context)

def orders(request:HttpRequest):
    context = {
        "orders_list": Order.objects.select_related("user").all()
    }
    return render(request, 'shopapp/order.html', context=context)