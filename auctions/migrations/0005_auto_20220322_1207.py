# Generated by Django 2.2.13 on 2022-03-22 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_remove_listing_status_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status_active',
            field=models.BooleanField(default='True'),
        ),
    ]
