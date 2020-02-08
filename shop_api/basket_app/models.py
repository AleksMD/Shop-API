from django.db import models
from django.contrib.auth.models import User


class Basket(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['owner']

    def __str__(self):
        name = self.owner.get_full_name()
        return f'Basket of customer: {name}'


class Discount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discount_percent = models.DecimalField(max_digits=3,
                                           decimal_places=2,
                                           default=0)

    class Meta:
        ordering = ['user', 'discount_percent']

    def __str__(self):
        discount = int(100 * self.discount_percent)
        return (f"User: {self.user.username} has discount "
                f"{discount} %")
