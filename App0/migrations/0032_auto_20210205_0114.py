# Generated by Django 3.1.5 on 2021-02-04 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0031_orders_discount_per'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image_0',
            field=models.ImageField(upload_to='lost-empire/'),
        ),
        migrations.AlterField(
            model_name='products',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='lost-empire/'),
        ),
    ]
