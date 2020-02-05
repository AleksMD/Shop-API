from django.test import TestCase, tag
from shop_app.models import Shop


class TestShopModel(TestCase):

    def setUp(self):

        self.shop_1 = Shop.objects.create(name='Amigo',
                                          city='Madrid',
                                          owner='Homer Sanchez')

        self.shop_2 = Shop.objects.create(name='Grocery',
                                          city='Boston',
                                          owner='Emily Smith')
        self.shop_3 = {'name': 'Racoon',
                       'city': 'Kharkiv',
                       'owner': 'Anna Melnyk'}

    @tag('query_shop')
    def test_quering_shops_from_db(self):
        all_shops = Shop.objects.all()
        self.assertEqual(len(all_shops), 2)
        first_shop = Shop.objects.first()
        self.assertEqual(first_shop.name, 'Amigo')
        filtered_query = Shop.objects.filter(city='Boston').all()
        self.assertEqual(len(filtered_query), 1)
        self.assertEqual(filtered_query[0].name, 'Grocery')

    @tag('create_shop')
    def test_create_shop_in_db(self):
        Shop.objects.create(**self.shop_3)
        shops = Shop.objects.all()
        self.assertEqual(len(shops), 3)
        self.assertEqual(shops[len(shops)-1].city, 'Kharkiv')
        self.assertEqual(shops[len(shops)-1].name, 'Racoon')
        self.assertEqual(shops[len(shops)-1].owner, 'Anna Melnyk')

    @tag('shop_fields')
    def test_shop_fields(self):
        self.assertEqual(self.shop_1.name, 'Amigo')
        self.assertEqual(self.shop_1.city, 'Madrid')
        self.assertEqual(self.shop_1.owner, 'Homer Sanchez')
        self.assertEqual(self.shop_2.name, 'Grocery')
        self.assertEqual(self.shop_2.city, 'Boston')
        self.assertEqual(self.shop_2.owner, 'Emily Smith')
