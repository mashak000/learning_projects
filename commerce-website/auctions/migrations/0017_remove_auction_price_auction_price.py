# Generated by Django 5.0.1 on 2024-01-31 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auction_winner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='price',
        ),
        migrations.AddField(
            model_name='auction',
            name='price',
            field=models.ManyToManyField(related_name='bids', to='auctions.bid'),
        ),
    ]