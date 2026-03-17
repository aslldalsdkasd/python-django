from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Creating Orders')
        user = User.objects.get(username='admin')
        order = Order.objects.get_or_create(
            promocode = "123w",
            delivery_address = "st STeerr",
            user = user
        )

        self.stdout.write(
            self.style.SUCCESS('Successfully created Order')
        )