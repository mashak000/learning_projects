# Generated by Django 5.0.1 on 2024-02-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_remove_like_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.URLField(blank=True),
        ),
    ]
