from django.contrib import admin
from basket_app.models import Basket, Discount


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'active')
    search_fields = ('owner', 'active')
    list_filter = ('owner', 'active')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user', 'discount_percent')
    search_fields = ('user', 'discount_percent')
    list_filter = ('user', 'discount_percent')
