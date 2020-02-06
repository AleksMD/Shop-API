from django.test import TestCase, tag, Client
from basket_app.models import Basket
from django.contrib.auth.models import User, Permission
from product_app.models import Product
from django.http import QueryDict
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType


class TestBasketViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             first_name='test_first_name',
                                             last_name='test_last_name',
                                             email='test@gmail.com',
                                             password='test_password')
        # Grants permission for user to change basket
        get_permission = Permission.objects.get(codename='change_basket')
        self.user.user_permissions.add(get_permission)
        self.user.save()

        self.client = Client()
        # Creating product samples in database
        prod_field_name = ('name', 'price',
                           'description', 'category',
                           'shop', 'available')
        prod_set = [('apple', '12.40', 'green', 'fruits', None, True),
                    ('carrot', '32.50', 'orange', 'vegetables', None, False),
                    ('ball', '51.00', 'red', 'toys', None, False)]
        self.products = [dict(zip(prod_field_name, item)) for item in prod_set]
        for product in self.products:
            Product.objects.create(**product)
        self.product_set = Product.objects.all()
        self.query_str = QueryDict(mutable=True)

    @tag('user_add_prod_to_basket')
    def test_user_add_product_to_basket(self):
        basket = Basket(owner=self.user)
        basket.save()
        self.client.login(username=self.user.username,
                          password='test_password')
        response = self.client.get(reverse('add_prod_to_bask',
                                           kwargs={'prod_pk': 1}))
        data_to_compare = response.json()[0]['fields']
        self.assertEqual(response.status_code, 200)
        self.assertIn('apple', data_to_compare.values())
        self.assertIn('price', data_to_compare.keys())
        self.assertEqual(data_to_compare['price'], '12.40')
