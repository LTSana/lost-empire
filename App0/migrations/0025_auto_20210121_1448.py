# Generated by Django 3.1.5 on 2021-01-21 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0024_orders_discount_per'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='paypal_auth',
            field=models.CharField(blank=True, help_text="PayPal's Authorization ID to capture the funds. (We currently don't need this)", max_length=999, null=True),
        ),
    ]
