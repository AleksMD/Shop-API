from decimal import Decimal
import json
from django.test import TestCase, tag, Client
from basket_app.models import Basket, Discount
from django.contrib.auth.models import User, Permission
from product_app.models import Product
from django.urls import reverse
from django.conf import settings


class TestBasketViews(TestCase):

    fixtures = settings.FIXTURES

    def setUp(self):

        self.user = User.objects.create_user(username='test_user',
                                             first_name='test_first_name',
                                             last_name='test_last_name',
                                             email='test@gmail.com',
                                             password='test_password')
        # Grants permission for user to change basket
        change_basket_perm = Permission.objects.get(codename='change_basket')
        view_basket_perm = Permission.objects.get(codename='view_basket')
        self.user.user_permissions.add(view_basket_perm, change_basket_perm)
        self.user.save()

        self.client = Client()
        self.basket = Basket.objects.create(owner=self.user)
        self.user_discount = Discount.objects.create(user=self.user)
        self.product_set = Product.objects.all()

    @tag('user_add_prod_to_basket')
    def test_user_add_product_to_basket(self):
        self.client.login(username=self.user.username,
                          password='test_password')
        response = self.client.get(reverse('add_prod_to_bask',
                                           kwargs={'prod_pk': 1}))
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()[0]['fields']
        self.assertIn('apple', data_to_compare.values())
        self.assertIn('price', data_to_compare.keys())
        self.assertEqual(data_to_compare['price'], '12.40')

    @tag('view_active_basket')
    def test_user_look_through_basket(self):
        user_basket = self.user.basket_set.get(active=True)
        user_basket.product_set.add(self.product_set[0])
        user_basket.product_set.add(self.product_set[1])
        self.client.login(username=self.user.username,
                          password='test_password')
        response = self.client.get(reverse('view_active_basket'))
        self.assertEqual(response.status_code, 200)
        data_to_compare = [item['fields'] for item in response.json()]
        self.assertIn('ball', data_to_compare[1].values())
        self.assertIn('apple', data_to_compare[0].values())

    @tag('add_to_basket_unauth')
    def test_unauth_user_add_product_to_basket(self):
        response = self.client.get(reverse('add_prod_to_bask',
                                           kwargs={'prod_pk': 1}))
        self.assertEqual(response.status_code, 302)

    @tag('view_active_basket_unauth')
    def test_unauth_user_view_basket(self):
        response = self.client.get(reverse('view_active_basket'))
        self.assertEqual(response.status_code, 302)

    @tag('view_empty_basket')
    def test_user_view_empty_basket(self):
        self.client.login(username=self.user.username,
                          password='test_password')
        response = self.client.get(reverse('view_active_basket'))
        self.assertEqual(response.status_code, 404)
        content = str(response.content, encoding='utf-8')
        self.assertInHTML('Your basket is empty', content)

    @tag('get_total_basket_price')
    def test_user_get_total_price_of_prod_in_basket(self):
        user_basket = self.user.basket_set.get(active=True)
        user_basket.product_set.add(self.product_set[0])
        user_basket.product_set.add(self.product_set[1])
        self.client.login(username=self.user.username,
                          password='test_password')
        response = self.client.get(reverse('view_total_basket_price'))
        self.assertEqual(response.status_code, 200)
        content = {k: json.loads(v) for k, v in response.json().items()}
        total_price_from_resp = content['total_cost']['total']
        total_price_from_model = self.product_set[0].price +\
            self.product_set[1].price
        price_to_compare = Decimal(
            total_price_from_resp).quantize(Decimal('1.00'))
        self.assertEqual(price_to_compare, total_price_from_model)

    @tag('user_discount')
    def test_total_price_with_user_discount(self):
        user_basket = self.user.basket_set.get(active=True)
        self.user_discount.discount_percent = 0.1
        self.user_discount.save()
        self.user_discount.refresh_from_db()
        user_basket.product_set.add(self.product_set[0])
        user_basket.product_set.add(self.product_set[1])
        self.client.login(username=self.user.username,
                          password='test_password')
        response = self.client.get(reverse('view_total_basket_price'))
        self.assertEqual(response.status_code, 200)
        content = {k: json.loads(v) for k, v in response.json().items()}

        # retrieve data(price in this case) from db for further processing
        total_price_from_resp = content['total_cost']['total']
        total_price_without_disc = (self.product_set[0].price +
                                    self.product_set[1].price)
        total_price_with_disc = (total_price_without_disc -
                                 total_price_without_disc *
                                 self.user.discount.discount_percent)

        # quantize method allows to define number
        # of digits after point
        # For instance: Decimal(1.0934343434).quantize(Decimal('1.00') will
        # return  Decimal('1.09')
        total_price_with_disc = Decimal(
            total_price_with_disc).quantize(Decimal('1.00'))
        price_to_compare = Decimal(
            total_price_from_resp).quantize(Decimal('1.00'))

        self.assertEqual(price_to_compare, total_price_with_disc)

    @tag('user_pay_for_basket_posit')
    def test_user_pay_for_basket_positive_case(self):
        # Add product to the basket
        user_basket = self.user.basket_set.get(active=True)
        user_basket.product_set.add(self.product_set[0])
        user_basket.product_set.add(self.product_set[1])
        # Emulates login process
        self.client.login(username=self.user.username,
                          password='test_password')
        data = json.dumps({'money': 63.4})
        response = self.client.post(reverse('pay_for_products'),
                                    data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        content = str(response.content, encoding='utf-8')
        self.assertInHTML('Transaction was successfull', content)

    @tag('user_pay_for_basket_neg')
    def test_user_pay_for_basket_negative_case(self):
        # Add product to the basket
        user_basket = self.user.basket_set.get(active=True)
        user_basket.product_set.add(self.product_set[0])
        user_basket.product_set.add(self.product_set[1])
        # Emulates login process
        self.client.login(username=self.user.username,
                          password='test_password')
        data = json.dumps({'money': 33.4})
        response = self.client.post(reverse('pay_for_products'),
                                    data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        content = str(response.content, encoding='utf-8')
        self.assertInHTML('The sum of money you have sent is not enough',
                          content)

    @tag('user_sent_extra_money')
    def test_user_pay_more(self):
        # Add product to the basket
        user_basket = self.user.basket_set.get(active=True)
        user_basket.product_set.add(self.product_set[0])
        user_basket.product_set.add(self.product_set[1])
        # Emulates login process
        self.client.login(username=self.user.username,
                          password='test_password')
        data = json.dumps({'money': 133.4})
        response = self.client.post(reverse('pay_for_products'),
                                    data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        message = "You still have some money: 70.00! "\
                  "Would you like to buy something else?"
        content = str(response.content, encoding='utf-8')
        self.assertInHTML(message, content)
