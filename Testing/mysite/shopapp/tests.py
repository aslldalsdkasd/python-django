from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from shopapp.models import Order, Product


# Create your tests here.

class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='admin', password='qwerty')
        permission = Permission.objects.get(codename='view_order', content_type__app_label='shopapp')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.product = Product.objects.create(
            name='Test Product',
            price=100
        )
        self.order = Order.objects.create(
            delivery_address='ul78',
            promocode='123',
            user_id=self.user.pk
        )
        self.order.products.set([self.product.id])


    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        url = reverse('shopapp:order_details', kwargs={'pk': self.order.pk})
        response = self.client.get(url)


        self.assertContains(response, 'ul78')
        self.assertContains(response, '123')
        self.assertEqual(response.context['order'].pk, self.order.pk)



class OrdersExportTestCase(TestCase):
    fixtures = [
        'user.json',
        'order.json',
        'products.json',
    ]
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_superuser(username='adminddd', password='qwertt')



    def setUp(self):
        self.client.force_login(self.user)
        user = User.objects.get(username='admin')
        self.client.force_login(user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_order_export(self):
        url = reverse('shopapp:order_export')
        response = self.client.get(url)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user.id if order.user else None,
                'products': [product.id for product in order.products.all()]
            }
            for order in orders
        ]
        orders_data = response.json()
        print(f'orders_data: {orders_data}')
        print(f'expected_data: {expected_data}')
        self.assertEqual(orders_data['orders'], expected_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')


