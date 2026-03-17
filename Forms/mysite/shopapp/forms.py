from django import forms

from shopapp.models import Product, Order


class ProductCreateForm(forms.ModelForm):
    price = forms.DecimalField(min_value=0.01)
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount'

class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'promocode', 'user', 'products']  # Список!
        widgets = {
            'delivery_address': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
        }