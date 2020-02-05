from django.test import TestCase, Client, tag
from django.urls import reverse
from product_app.models import Product
from shop_app.models import Shop
from django.contrib.auth.models import User


class TestProductViews(TestCase):

    def setUp(self):
        self.customer = User.objects.create_user('cusomer_username',
                                                 email='cust@gmail.com',
                                                 password='cust_password')
        self.admin = User.objects.create_superuser('admin',
                                                   email='admin@gmail.com',
                                                   password='admin_password')
        self.client = Client()
        prod_field_name = ('name', 'price',
                           'description', 'category',
                           'shop', 'available')
        prod_set = [('apple', '12.40', 'green', 'fruits', None, False),
                    ('carrot', '32.50', 'orange', 'vegetables', None, False),
                    ('ball', '51.00', 'red', 'toys', None, False)]
        self.products = [dict(zip(prod_field_name, item)) for item in prod_set]
        for product in self.products:
            Product.objects.create(**product)

    @tag('product_list')
    def test_get_list_of_all_products(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()
        self.assertEqual(len(data_to_compare), 3)
        self.assertEqual(data_to_compare[0]['fields'], self.products[0])

    @tag('detail_product')
    def test_get_detail_product(self):
        response = self.client.get(reverse('detail_product', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()
        self.assertEqual(len(data_to_compare), 1)
        self.assertEqual(data_to_compare[0]['fields'], self.products[1])

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
        self.assertEqual(product.price, 99.99)




