# Generated by Django 3.0.3 on 2020-02-08 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket_app', '0004_auto_20200208_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=3, null=True, verbose_name='user_discount'),
        ),
    ]
