# Generated by Django 3.1.5 on 2021-01-18 14:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0020_orders_date_made'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='date_made',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
