from .forms import CSVOrdersImport, CSVOrdersExport
from io import TextIOWrapper
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from django.urls import path
from csv import DictReader, writer
from django.contrib.auth.models import User

class OrderInline(admin.TabularInline):
    model = Product.orders.through


class ProductInline(admin.StackedInline):
    model = ProductImage


@admin.action(description="Archive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description="Unarchive products")
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):

    actions = [
        mark_archived,
        mark_unarchived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
        ProductInline,
    ]
    # list_display = "pk", "name", "description", "price", "discount"
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    ordering = "-name", "pk"
    search_fields = "name", "description"
    fieldsets = [
        (None, {
           "fields": ("name", "description"),
        }),
        ("Price options", {
            "fields": ("price", "discount"),
            "classes": ("wide", "collapse"),
        }),
        ("Images", {
            "fields": ("preview", ),
        }),
        ("Extra options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": "Extra options. Field 'archived' is for soft delete",
        })
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


# admin.site.register(Product, ProductAdmin)


# class ProductInline(admin.TabularInline):
class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    change_list_template = "shopapp/orders_changeslist.html"
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"

    def get_queryset(self, request):
        return Order.objects.select_related("user").prefetch_related("products")

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username

    def import_csv(self, request:HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVOrdersImport()
            context = {
                "form": form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVOrdersImport(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)

        csv_file = TextIOWrapper(
            form.files['csv_file'].file,
            encoding=request.encoding,
                                 )
        reader = DictReader(csv_file)
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items() if k}
            user = User.objects.get(username=row["user"])
            order = Order.objects.create(
                delivery_address=row["delivery_address"],
                promocode=row.get('promocode', ''),
                user=user,
            )

            if row.get("products"):
                products_name = [p.strip() for p in row["products"].split(",")]
                for name in products_name:
                    product = Product.objects.get(name=name)
                    order.products.add(product)
        self.message_user(request, "Successfully imported products.")
        return redirect('..')

    actions = ['export_csv']  # ← добавить для actions
    change_actions = ['export_csv']
    def export_csv(self, request:HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVOrdersExport()
            context = {
                "form": form,
            }
            return render(request, 'admin/csv_export.html', context)
        form = CSVOrdersExport(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, 'admin/csv_export.html', context, status=400)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        csv_writer = writer(response)
        csv_writer.writerow([
            'user', 'delivery_address', 'promocode', 'products',
        ])
        for order in Order.objects.all():
            csv_writer.writerow([
                order.user.username,
                order.delivery_address,
                order.promocode,
                ', '.join([p.name for p in order.products.all()]),
            ])
        self.message_user(request, "Successfully exported orders.")
        return response




    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import_orders_csv/', self.import_csv, name="import_orders_csv"),
            path('export_csv/', self.export_csv, name="export_csv"),
        ]
        return new_urls + urls
