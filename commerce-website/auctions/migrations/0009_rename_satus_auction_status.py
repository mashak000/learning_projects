# Generated by Django 5.0.1 on 2024-01-29 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auction_satus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='satus',
            new_name='status',
        ),
    ]