# Generated by Django 3.0.3 on 2020-02-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basket_app', '0006_auto_20200208_1254'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'ordering': ['user', 'discount_percent']},
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
    ]
