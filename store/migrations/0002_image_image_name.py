# Generated by Django 4.0.1 on 2022-03-16 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image_name',
            field=models.CharField(default='book_img', max_length=255),
        ),
    ]
