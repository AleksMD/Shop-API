from django.test import TestCase, tag
from product_app.models import Product
from decimal import Decimal


class TestProductModel(TestCase):

    def setUp(self):

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

        self.product_3 = {'name': 'Tesla Model Y',
                          'price': 49999.99,
                          'category': 'Cars',
                          'description': 'The state-of-the-art electrocar'}

    @tag('query_product')
    def test_quering_products_from_db(self):
        all_products = Product.objects.all()
        self.assertEqual(len(all_products), 2)
        first_product = Product.objects.first()
        self.assertEqual(first_product.name, 'Apple')
        filtered_query = Product.objects.filter(name='Ball').all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, 'Ball')

    @tag('create_product')
    def test_create_product_in_db(self):
        Product.objects.create(**self.product_3)
        products = Product.objects.all()
        self.assertIsInstance(products[len(products)-1].price, Decimal)
        self.assertEqual(len(products), 3)
        self.assertEqual(products[len(products)-1].name, 'Tesla Model Y')
        self.assertEqual(products[len(products)-1].price,
                         Decimal(49999.99).quantize(Decimal('1.00')))
        self.assertEqual(products[len(products)-1].category, 'Cars')
        self.assertEqual(products[len(products)-1].description,
                         'The state-of-the-art electrocar')
