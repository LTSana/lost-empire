# Generated by Django 3.1.5 on 2021-01-20 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0021_products_date_made'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='denied_msg',
            field=models.CharField(blank=True, max_length=1600, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='refund_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]