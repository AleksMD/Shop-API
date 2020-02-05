from django.urls import path
from product_app.views import (create_new_product_in_db,
                               get_list_of_all_products,
                               update_existing_product,
                               delete_product_from_db,
                               get_particular_product)


urlpatterns = [path('product-list/',
                    get_list_of_all_products,
                    name='product_list'),
               path('detail-product/<int:pk>',
                    get_particular_product,
                    name='detail_product'),
               path('create-product/',
                    create_new_product_in_db,
                    name='create_product'),
               path('update-product/<int:pk>',
                    update_existing_product,
                    name='update_product'),
               path('delete-product/<int:pk>',
                    delete_product_from_db,
                    name='delete_product')]
