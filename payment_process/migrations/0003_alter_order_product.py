# Generated by Django 5.0 on 2024-11-05 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment_process', '0002_alter_order_product'),
        ('product', '0002_product_description_1_product_description_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='product.product', verbose_name='Ürün'),
        ),
    ]