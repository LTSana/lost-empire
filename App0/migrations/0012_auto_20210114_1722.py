# Generated by Django 3.1.5 on 2021-01-14 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0011_auto_20210114_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='available_sizes',
            field=models.JSONField(blank=True, default=[{'sizes': []}], null=True),
        ),
    ]
