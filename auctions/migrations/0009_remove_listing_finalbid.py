# Generated by Django 2.2.13 on 2022-03-22 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20220322_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='finalBid',
        ),
    ]