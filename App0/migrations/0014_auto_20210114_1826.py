# Generated by Django 3.1.5 on 2021-01-14 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0013_auto_20210114_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='available_sizes',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]