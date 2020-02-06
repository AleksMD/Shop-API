from django.urls import path
from basket_app.views import (get_list_of_all_user_baskets,
                              add_product_to_basket)

urlpatterns = [path('user-basket-list/',
                    get_list_of_all_user_baskets,
                    name='user_basket_list'),
               path('add-product-to-basket/<int:prod_pk>',
                    add_product_to_basket,
                    name='add_prod_to_bask')]
