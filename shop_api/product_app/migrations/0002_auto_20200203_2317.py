# Generated by Django 3.0.3 on 2020-02-03 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basket_app', '0001_initial'),
        ('product_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='basket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='basket_app.Basket'),
        ),
    ]
