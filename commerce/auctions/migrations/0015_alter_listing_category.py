# Generated by Django 4.1 on 2022-09-10 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Antiques', 'Antiques'), ('Electronics', 'Electronics'), ('Machinery', 'Machinery'), ('Fashion', 'Fashion'), ('Home', 'Home'), ('Sports', 'Sports'), ('Retail', 'Retail'), ('Toys', 'Toys'), ('Tools', 'Tools'), ('Vehicles', 'Vehicles'), ('Recreation', 'Recreation')], max_length=11),
        ),
    ]
