from django.contrib import admin
from product_app.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available',
                    'shop')
    list_filter = ('name', 'price', 'available',
                   'category', 'description', 'shop')
    search_fields = ('name', 'price', 'available',
                     'category', 'description', 'shop')
