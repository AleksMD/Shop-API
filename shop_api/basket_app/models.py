from django.db import models
from django.contrib.auth.models import User


class Basket(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        name = self.user.get_full_name()
        return f'Basket of customer: {name}'
