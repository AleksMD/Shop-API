from django.db import models


class Shop(models.Model):
    city = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'Shop: name={self.name}, city={self.city}'
