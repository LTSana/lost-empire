# Generated by Django 3.1.5 on 2021-01-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0014_auto_20210114_1826'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('percentage', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paypal_auth', models.CharField(max_length=999)),
                ('paypal_order_id', models.CharField(max_length=999)),
                ('paypal_data', models.JSONField()),
                ('cart_data', models.JSONField()),
                ('country', models.CharField(max_length=1600)),
                ('subtotal', models.FloatField(default=0)),
                ('shipping_cost', models.FloatField(default=0)),
            ],
        ),
    ]
