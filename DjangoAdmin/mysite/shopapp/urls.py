from .views import index, product, orders
from django.urls import path, include

app_name = 'shopapp'
urlpatterns = [
    path('', index, name='index'),
    path('product/', product, name='product'),
    path('orders/', orders, name='orders'),
]
