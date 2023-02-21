# Generated by Django 4.1 on 2022-09-10 07:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_remove_listing_watchlist_listing_watching'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]