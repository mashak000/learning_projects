# Generated by Django 5.0.1 on 2024-01-31 08:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='winner',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='winnerlistings', to=settings.AUTH_USER_MODEL),
        ),
    ]
