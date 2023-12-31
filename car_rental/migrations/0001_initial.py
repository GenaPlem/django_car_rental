# Generated by Django 4.2.7 on 2023-11-01 12:55

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('seats', models.IntegerField()),
                ('color', models.CharField(max_length=20)),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('car_image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_rental.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
