# Generated by Django 3.1.5 on 2021-01-21 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0030_remove_orders_discount_per'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='discount_per',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]