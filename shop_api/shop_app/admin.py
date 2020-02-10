from django.contrib import admin
from shop_app.models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_filter = ('city', 'name', 'owner')
    list_display = ('city', 'name')
    search_fields = ('city', 'name', 'owner')
