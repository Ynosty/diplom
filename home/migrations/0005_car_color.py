# Generated by Django 4.0.2 on 2022-06-18 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_car_images2_car_images3_car_images4_car_images5_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]