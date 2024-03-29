# Generated by Django 4.1 on 2022-08-20 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=150)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='all_commenters', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='static/auctions')),
                ('description', models.CharField(max_length=1000)),
                ('bid', models.FloatField(blank=True, null=True)),
                ('StartingBid', models.FloatField()),
                ('category', models.CharField(choices=[('Antiques', 'Antiques'), ('Electronics', 'Electronics'), ('Machinery', 'Machinery'), ('Fashion', 'Fashion'), ('Home', 'Home'), ('Sports', 'Sports'), ('Retail', 'Retail'), ('Toys', 'Toys'), ('Tools', 'Tools'), ('Vehicles', 'Vehicles'), ('Recreation', 'Recreation')], default='Antiques', max_length=11)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_creators', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='AuctionListing',
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='all_listings', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_bidders', to=settings.AUTH_USER_MODEL),
        ),
    ]
