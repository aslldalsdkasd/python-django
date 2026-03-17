from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(null=False, max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    discount = models.PositiveSmallIntegerField(null=False, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)



class Order(models.Model):
    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ManyToManyField(Product, related_name='orders')

