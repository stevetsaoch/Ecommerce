# Generated by Django 4.0.1 on 2022-03-07 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_address_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='delivery_instructions',
            field=models.CharField(blank=True, max_length=255, verbose_name='Delivery Instructions'),
        ),
    ]
