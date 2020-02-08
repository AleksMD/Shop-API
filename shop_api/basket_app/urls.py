from django.urls import path
from basket_app.views import (get_list_of_all_user_baskets,
                              add_product_to_basket,
                              view_active_basket,
                              view_total_basket_price,
                              user_payment_view)

urlpatterns = [path('user-basket-list/',
                    get_list_of_all_user_baskets,
                    name='user_basket_list'),
               path('add-product-to-basket/<int:prod_pk>',
                    add_product_to_basket,
                    name='add_prod_to_bask'),
               path('view-active-basket',
                    view_active_basket,
                    name='view_active_basket'),
               path('view-total-basket-price',
                    view_total_basket_price,
                    name='view_total_basket_price'),
               path('pay-for-products',
                    user_payment_view,
                    name='pay_for_products')]
