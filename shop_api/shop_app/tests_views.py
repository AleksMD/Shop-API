from django.test import TestCase, tag, Client
from django.contrib.auth.models import User
from shop_app.models import Shop
from django.http import QueryDict
from django.urls import reverse


class TestShopViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin_user',
            first_name='admin_first_name',
            last_name='admin_last_name',
            email='admin@gmail.com',
            password='admin_password')
        # Creating shop samples in database
        shop_field_name = ('name', 'city', 'owner')
        shop_set = [('Jewelery', 'Paris', 'Monty Python'),
                    ('Apricot', 'London', 'Eric Idle'),
                    ('Grocery', 'New York', 'Raymond Hettinger')]
        self.shops = [dict(zip(shop_field_name, item)) for item in shop_set]
        for shop in self.shops:
            Shop.objects.create(**shop)
        self.query_str = QueryDict(mutable=True)

    @tag('admin_add_new_shop')
    def test_admin_add_new_shop(self):
        self.client.login(username=self.admin.username,
                          password='admin_password')
        data = {'name': 'Meet&Fish', 'city': 'Kiyv', 'owner': 'Ivan Bohun'}
        response = self.client.post(reverse('add_new_shop'),
                                    data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        shop = Shop.objects.filter(name='Meet&Fish').all()
        self.assertEqual(len(shop), 1)
        self.assertEqual(shop[0].city, 'Kiyv')
        self.assertEqual(shop[0].owner, 'Ivan Bohun')

    @tag('admin_change_exist_shop')
    def test_admin_change_exist_shop(self):
        self.client.login(username=self.admin.username,
                          password='admin_password')
        data = {'name': 'Meet&Fish', 'city': 'Kiyv', 'owner': 'Ivan Bohun'}
        response = self.client.put(reverse('change_existing_shop',
                                           kwargs={'shop_pk': 1}),
                                   data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        all_shops = Shop.objects.all()
        shop = Shop.objects.filter(name='Meet&Fish').all()
        self.assertEqual(len(all_shops), 3)
        self.assertEqual(len(shop), 1)
        self.assertEqual(shop[0].city, 'Kiyv')
        self.assertEqual(shop[0].owner, 'Ivan Bohun')

    @tag('show_particular_shop')
    def test_get_particular_shop(self):
        response = self.client.get(reverse('get_particular_shop',
                                           kwargs={'shop_pk': 2}))
        self.assertEqual(response.status_code, 200)
        data_to_compare = response.json()[0]['fields']
        self.assertEqual(data_to_compare['name'], self.shops[1]['name'])
        self.assertEqual(data_to_compare['owner'], self.shops[1]['owner'])
        self.assertEqual(data_to_compare['city'], self.shops[1]['city'])

    @tag('show_shops_list')
    def test_get_list_of_all_shops(self):
        response = self.client.get(reverse('get_shop_list'))
        self.assertEqual(response.status_code, 200)
        data_to_compare = [shop['fields'] for shop in response.json()]
        # returned data ordered by name
        self.assertEqual(data_to_compare[0], self.shops[1])
        self.assertEqual(data_to_compare[1], self.shops[2])
        self.assertEqual(data_to_compare[2], self.shops[0])
