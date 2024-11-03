# Generated by Django 4.1.7 on 2023-05-28 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_shippingaddress_days_alter_shippingaddress_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='fuel_economy_rating',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='car',
            name='off_road_performance_rating',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='car',
            name='repair_cost_rating',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
