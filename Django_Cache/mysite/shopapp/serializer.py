
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = ['id', 'delivery_address', 'promocode', 'products', 'user']