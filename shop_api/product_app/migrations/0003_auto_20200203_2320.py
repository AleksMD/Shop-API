# Generated by Django 3.0.3 on 2020-02-03 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0001_initial'),
        ('product_app', '0002_auto_20200203_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shop',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop_app.Shop'),
        ),
    ]
