# Generated by Django 2.2.13 on 2022-03-22 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_status_listed'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='mine',
            field=models.BooleanField(default='False'),
        ),
    ]
