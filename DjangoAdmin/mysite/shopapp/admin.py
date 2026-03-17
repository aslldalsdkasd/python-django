from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from .admin_mixin import ExportAsCSVMixin
from shopapp.models import Product, Order


# Register your models here.

@admin.action(description='Archive Products')
def archive_products(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)

@admin.action(description="Anarchive Products")
def anrchive_products(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)

class OrderInline(admin.StackedInline):
    model = Product.orders.through

@admin.register(Product)
class AdminProduct(admin.ModelAdmin, ExportAsCSVMixin):
    actions = [
        anrchive_products,
        archive_products,
        "export_as_csv",
    ]
    inlines = [
        OrderInline,
    ]
    fieldsets = [
        (None,{
            'fields': ['name', 'description']
        }),
        ('price_setting', {
            'fields': ['price', 'discount']
        }),
        ('archived_setting', {
            'fields': ['archived'],
            'classes': ['collapse']
        }),
    ]
    list_display = ('pk', 'name', 'description_short' , 'price', 'discount', 'archived')
    list_display_links = ('pk', 'name')
    search_fields = ('name', 'price')


class ProductInline(admin.TabularInline):
    model = Order.product.through

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):

    inlines = [
        ProductInline,
    ]
    list_display = ('delivery_address', 'promocode', 'created_at', 'user_check')

    def user_check(self, obj:Order) -> str:
        return obj.user.username or obj.user.first_name

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('product')


