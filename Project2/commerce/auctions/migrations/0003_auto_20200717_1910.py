# Generated by Django 3.0.8 on 2020-07-17 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_bid_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='categories',
            field=models.CharField(blank=True, choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home'), ('Sporting Goods', 'Sports'), ('Vehicles', 'Vehicled')], max_length=16),
        ),
    ]
