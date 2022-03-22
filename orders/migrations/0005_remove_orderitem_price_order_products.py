# Generated by Django 4.0.1 on 2022-03-22 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_click_counter'),
        ('orders', '0004_remove_orderitem_product_orderitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='order_product', to='store.Product'),
        ),
    ]
