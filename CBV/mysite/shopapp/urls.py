from django.urls import path

from .views import (shop_index,
                    groups_list,
                    products_list,
                    OrderListView,
                    OrderDetailView,
                    ProductDetailView,
                    CreateProductView,
                    UpdateProductView,
                    DeleteProductView,
                    CreateOrderView,
                    UpdateOrderView,
                    DeleteOrderView,
                    ProductListView
                    )

app_name = "shopapp"

urlpatterns = [
    path("", shop_index, name="index"),
    path("groups/", groups_list, name="groups_list"),
    path("products/", ProductListView.as_view(), name="products_list"),
    path('products/create/', CreateProductView.as_view(), name='create_product'),
    path('products/<int:pk>/update/', UpdateProductView.as_view(), name='update_product'),
    path('products/<int:pk>/delete/', DeleteProductView.as_view(), name='delete_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
    path("orders/", OrderListView.as_view(), name="orders_list"),
    path('orders/create/', CreateOrderView.as_view(), name='create_order'),
    path('orders/<int:pk>/delete/', DeleteOrderView.as_view(), name='delete_order'),
    path('orders/<int:pk>/update/', UpdateOrderView.as_view(), name='update_order'),
    path("orders/<int:pk>/>", OrderDetailView.as_view(), name="order_detail"),

]
