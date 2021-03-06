from django.db import models
from shop_app.models import Shop
from basket_app.models import Basket


class Product(models.Model):

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    available = models.BooleanField(default=False)
    category = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField()
    shop = models.ForeignKey(Shop,
                             unique=False,
                             null=True,
                             on_delete=models.CASCADE)
    basket = models.ForeignKey(Basket,
                               blank=True,
                               null=True,
                               on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['name', 'price']

    def natural_key(self):
        return (self.name,) + self.shop.natural_key()

    natural_key.dependencies = ['shop_app.shop']

    def __str__(self):
        return (f'Product: name={self.name}, '
                f'price={self.price}, shop={self.shop}')
