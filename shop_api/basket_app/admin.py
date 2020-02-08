from django.contrib import admin
from basket_app.models import Basket, Discount

admin.register(Basket, Discount)
