# Generated by Django 3.0.8 on 2020-07-23 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_bid',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid_amount',
            field=models.FloatField(),
        ),
    ]