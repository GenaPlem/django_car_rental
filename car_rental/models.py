from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic')
    ]

    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electic', 'Electric'),
    ]

    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    seats = models.IntegerField()
    transmission_type = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES, default='manual')
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES, default='petrol')
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    car_image = CloudinaryField('image')
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.make} {self.model} ({self.year})'


class Booking(models.Model):
    INSURANCE_CHOICES = [
        ('young', 'Young (+50€)'),
        ('standart', 'Standart (+40€)'),
        ('senior', 'Senior (+60€)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=20, blank=False, null=False)
    surname = models.CharField(max_length=20, blank=False, null=False)
    child_seat = models.BooleanField(default=False)
    insurance_type = models.CharField(max_length=10, choices=INSURANCE_CHOICES, default='standart')
    rules_agreement = models.BooleanField(default=False, blank=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking for {self.car} by {self.name} {self.surname} ({self.user})"
