from django.urls import path
from shop_app.views import (add_new_shop_view,
                            change_existing_shop_view,
                            get_list_of_all_shops,
                            get_particular_shop)


urlpatterns = [path('add-new-shop/', add_new_shop_view,
                    name='add_new_shop'),
               path('change-exising-shop/<int:shop_pk>',
                    change_existing_shop_view,
                    name='change_existing_shop'),
               path('get-particular-shop/<int:shop_pk>',
                    get_particular_shop,
                    name='get_particular_shop'),
               path('get-list-with-all-shops/',
                    get_list_of_all_shops,
                    name='get_shop_list')]
