# Generated by Django 3.1.5 on 2021-01-14 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App0', '0007_auto_20210113_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='category',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
