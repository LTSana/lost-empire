# Generated by Django 3.1.5 on 2021-01-17 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0016_orders_hash_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_status',
            field=models.CharField(choices=[('WAITING', 'WAITING'), ('COMPLETE', 'COMPLETE'), ('DENIED', 'DENIED')], default='WAITING', max_length=9),
        ),
        migrations.AddField(
            model_name='orders',
            name='registered_user',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='tracker_id',
            field=models.CharField(blank=True, help_text='The tracker code given by the shipping company', max_length=1600, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='user_pk',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]