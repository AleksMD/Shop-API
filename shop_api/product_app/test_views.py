from django.test import TestCase, Client, tag
from django.urls import reverse
from product_app.models import Product
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict
from django.core import serializers
import json
from django.conf import settings


class TestProductViews(TestCase):

    fixtures = settings.FIXTURES

    def setUp(self):
        self.customer = User.objects.create_user('cusomer_username',
                                                 email='cust@gmail.com',
                                                 password='cust_password')
        self.admin = User.objects.create_superuser('admin',
                                                   email='admin@gmail.com',
                                                   password='admin_password')
        self.client = Client()
        self.products = serializers.serialize('json',
                                              Product.objects.all(),
                                              fields=['name', 'price',
                                                      'description',
                                                      'category',
                                                      'shop', 'available'],
                                              use_natural_foreign_keys=True)
        self.products = json.loads(self.products)
        self.query_str = QueryDict(mutable=True)

    @tag('product_list')
    def test_get_list_of_all_products(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()
        self.assertEqual(len(data_to_compare), 3)
        self.assertEqual(data_to_compare[0]['fields'],
                         self.products[0]['fields'])

    @tag('detail_product')
    def test_get_detail_product(self):
        response = self.client.get(reverse('detail_product', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()
        self.assertEqual(len(data_to_compare), 1)
        self.assertEqual(data_to_compare[0]['fields'],
                         self.products[2]['fields'])

    @tag('create_product_auth')
    def test_create_new_product_by_admin(self):
        self.client.login(username=self.admin.username,
                          password='admin_password')
        data = {'name': 'shirt', 'price': 104.99, 'description': 'white',
                'category': 'cloth', 'shop': None, 'available': False}
        response = self.client.post(reverse('create_product'),
                                    data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        products = Product.objects.all()
        self.assertEqual(len(products), 4)
        expected_message = "Product: name=shirt, price=104.99 was created."
        resp_content = str(response.content, encoding='utf-8')
        self.assertInHTML(expected_message, resp_content)

    @tag('create_product_unauth')
    def test_create_new_product_by_non_admin(self):
        self.client.login(username=self.customer.username,
                          password='cust_password')
        data = {'name': 'shirt', 'price': 104.99, 'description': 'white',
                'category': 'cloth', 'shop': None, 'available': False}
        response = self.client.post(reverse('create_product'),
                                    data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 302)

    @tag('update_product_auth')
    def test_update_product_by_admin(self):
        self.client.login(username=self.admin.username,
                          password='admin_password')
        data = {'price': 99.99, 'available': True}
        response = self.client.put(reverse('update_product',
                                           kwargs={'pk': 2}),
                                   data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 204)
        product = Product.objects.filter(pk=2).first()
        self.assertTrue(product.available)
        self.assertEqual(product.price,
                         Decimal(99.99).quantize(Decimal('1.00')))

    @tag('upd_prod_inv_val_auth')
    def test_update_product_by_admin_wrong_field(self):
        self.client.login(username=self.admin.username,
                          password='admin_password')
        data = {'wrong_field': 'Test', 'price': 99.99, 'available': True}
        response = self.client.put(reverse('update_product',
                                           kwargs={'pk': 2}),
                                   data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        product = Product.objects.filter(pk=2).first()
        self.assertTrue(product.available)
        self.assertEqual(product.price,
                         Decimal('32.50').quantize(Decimal('1.00')))

    @tag('upd_prod_unauth')
    def test_update_product_without_permissions(self):
        self.client.login(username=self.customer.username,
                          password='cust_password')
        data = {'price': 99.99, 'available': True}
        response = self.client.put(reverse('update_product',
                                           kwargs={'pk': 2}),
                                   data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 302)
        product = Product.objects.filter(pk=2).first()
        self.assertIsNotNone(product)
        self.assertTrue(product.available)
        self.assertEqual(product.price,
                         Decimal('32.50').quantize(Decimal('1.00')))

    @tag('delete_product_auth')
    def test_delete_existing_product_by_admin(self):
        self.client.login(username=self.admin.username,
                          password='admin_password')
        response = self.client.delete(reverse('delete_product',
                                      kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 204)
        products = Product.objects.all()
        self.assertEqual(len(products), 2)
        with self.assertRaises(ObjectDoesNotExist):
            Product.objects.get(pk=2)

    @tag('delete_non_exist_prod')
    def test_delete_unexisting_product_by_admin(self):
        self.client.login(username=self.admin.username,
                          password='admin_password')
        response = self.client.delete(reverse('delete_product',
                                      kwargs={'pk': 10}))
        self.assertEqual(response.status_code, 400)
        products = Product.objects.all()
        self.assertEqual(len(products), 3)

    @tag('del_prod_unauth')
    def test_delete_product_without_permissions(self):
        self.client.login(username=self.customer.username,
                          password='cust_password')
        response = self.client.delete(reverse('update_product',
                                              kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 302)
        products = Product.objects.all()
        self.assertEqual(len(products), 3)

    @tag('exact_prod_search')
    def test_exact_search_product(self):
        search_params = {'name': 'carrot'}
        self.query_str.update(search_params)
        query_str = '?' + self.query_str.urlencode()
        response = self.client.get(reverse('exact_search') + query_str)
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()
        self.assertEqual(len(data_to_compare), 1)
        self.assertEqual(data_to_compare[0]['fields'],
                         self.products[2]['fields'])

    @tag('approx_prod_search')
    def test_approximate_product_search(self):
        search_params = {'name': 'car',
                         'category': 'veget'}
        self.query_str.update(search_params)
        query_str = '?' + self.query_str.urlencode()
        response = self.client.get(reverse('approximate_search') + query_str)
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()
        self.assertEqual(len(data_to_compare), 1)
        self.assertEqual(data_to_compare[0]['fields'],
                         self.products[2]['fields'])

    @tag('search_prod_by_shop')
    def test_search_product_by_shop(self):
        search_params = {'name': 'Grocery'}
        self.query_str.update(search_params)
        query_str = '?' + self.query_str.urlencode()
        response = self.client.get(reverse('search_by_shop') + query_str)
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()
        self.assertEqual(len(data_to_compare), 1)
        self.assertEqual(data_to_compare[0]['fields'],
                         self.products[1]['fields'])

    @tag('search_prod_by_price_pos')
    def test_search_product_by_price_range_pos(self):
        search_params = {'from': 30, 'to': 60}
        self.query_str.update(search_params)
        query_str = '?' + self.query_str.urlencode()
        response = self.client.get(reverse('search_by_price') + query_str)
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()
        self.assertEqual(len(data_to_compare), 2)
        prod_1 = data_to_compare[0]['fields']
        prod_2 = data_to_compare[1]['fields']
        self.assertEqual(prod_1, self.products[2]['fields'])
        self.assertEqual(prod_2, self.products[1]['fields'])

    @tag('search_prod_by_price_neg')
    def test_search_product_by_price_range_negat(self):
        search_params = {'from': 130, 'to': 160}
        self.query_str.update(search_params)
        query_str = '?' + self.query_str.urlencode()
        response = self.client.get(reverse('search_by_price') + query_str)
        self.assertEqual(response.status_code, 404)

    @tag('search_prod_by_price_wr_typ')
    def test_search_product_by_price_wrong_type(self):
        search_params = {'from': 130, 'to': 'test'}
        self.query_str.update(search_params)
        query_str = '?' + self.query_str.urlencode()
        response = self.client.get(reverse('search_by_price') + query_str)
        self.assertEqual(response.status_code, 400)
