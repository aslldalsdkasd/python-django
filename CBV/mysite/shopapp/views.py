from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from .models import Product, Order



def shop_index(request: HttpRequest):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        "time_running": default_timer(),
        "products": products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)


def groups_list(request: HttpRequest):
    context = {
        "groups": Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)


def products_list(request: HttpRequest):
    context = {
        "products": Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)


# def orders_list(request: HttpRequest):
#     context = {
#         "orders": Order.objects.select_related("user").prefetch_related("products").all(),
#     }
#     return render(request, 'shopapp/orders-list.html', context=context)

class OrderListView(ListView):
    model = Order
    template_name = 'shopapp/orders-list.html'
    queryset = Order.objects.select_related("user").prefetch_related("products").all()
    context_object_name = 'orders'

class OrderDetailView(DetailView):
    queryset = (Order.objects
                .select_related("user")
                .prefetch_related("products")
                )

class CreateOrderView(CreateView):
    model = Order
    template_name = 'shopapp/orders-create.html'
    fields = ['delivery_address', 'promocode', 'products', 'user']
    success_url = reverse_lazy('shopapp:orders_list')

class UpdateOrderView(UpdateView):
    model = Order
    template_name = 'shopapp/orders-update.html'
    fields = ['delivery_address', 'promocode', 'products', 'user']
    success_url = reverse_lazy('shopapp:orders_list')

class DeleteOrderView(DeleteView):
    model = Order
    template_name = 'shopapp/orders-delete.html'
    success_url = reverse_lazy("shopapp:orders_list")

class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/products-detail.html'

class CreateProductView(CreateView):
    model = Product
    template_name = 'shopapp/products-create.html'
    fields = ['name', 'description', 'price', 'discount']
    success_url = reverse_lazy('shopapp:products_list')

class UpdateProductView(UpdateView):
    model = Product
    template_name = 'shopapp/products-update.html'
    fields = ['name', 'description', 'price', 'discount']
    success_url = reverse_lazy("shopapp:products_list")

class DeleteProductView(DeleteView):
    model = Product
    template_name = 'shopapp/products-delete.html'
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)
