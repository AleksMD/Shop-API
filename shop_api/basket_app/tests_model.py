from django.test import TestCase, tag
from django.contrib.auth.models import User
from basket_app.models import Basket
from django.db import IntegrityError
from product_app.models import Product


class TestBasketModel(TestCase):

    def setUp(self):
        self.owner = User.objects.create(username='ac_dc',
                                        first_name='Alice',
                                        last_name='Cooper',
                                        email='alcp@gmail.com')
        self.product_1 = Product.objects.create(
            name='Apple',
            price=15,
            category='Fruits',
            description='Fresh apples from Poland')

        self.product_2 = Product.objects.create(
            name='Ball',
            price=20.34,
            category='Toys',
            description='Round and multicolored.')

    @tag('create_empty_basket')
    def test_create_empty_basket_valid(self):
        Basket.objects.create(owner=self.owner)
        basket = Basket.objects.all()
        self.assertEqual(len(basket), 1)
        self.assertEqual(basket[0].owner, self.owner)
        self.assertEqual(basket[0].owner.username, self.owner.username)

    @tag('create_invalid_basket')
    def test_create_empty_basket_invalid(self):
        with self.assertRaises(IntegrityError):
            Basket.objects.create()

    @tag('product_to_from_basket')
    def test_add_remove_product_to_basket(self):
        Basket.objects.create(owner=self.owner)
        basket = Basket.objects.first()
        basket.product_set.add(self.product_1)
        basket.product_set.add(self.product_2)
        self.assertEqual(len(basket.product_set.all()), 2)
        self.assertEqual(basket.product_set.first().name,
                         self.product_1.name)
        self.assertEqual(basket.product_set.all()[1].name,
                         self.product_2.name)

        # asserts removing products from basket
        basket.product_set.remove(self.product_1)
        self.assertEqual(len(basket.product_set.all()), 1)
        self.assertEqual(basket.product_set.all()[0].name,
                         self.product_2.name)

    @tag('create_several_baskets')
    def test_user_creates_several_basket(self):
        Basket.objects.create(owner=self.owner)
        Basket.objects.create(owner=self.owner)
        self.assertEqual(len(self.owner.basket_set.all()), 2)
        baskets = Basket.objects.filter(owner=self.owner).all()
        self.assertEqual(len(baskets), 2)
