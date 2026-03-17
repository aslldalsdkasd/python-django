from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Creating product')

        product_list = [
            ('Laptop', 3000),
            ('Apple', 6000),
            ('Mouse', 5000),
        ]

        for name, price in product_list:
            product, created =Product.objects.get_or_create(name= name, defaults={'price': price}  )

            self.stdout.write(f'Product created {name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created the product')
        )
