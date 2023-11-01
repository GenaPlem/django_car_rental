from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Car(models.Model): 
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    seats = models.IntegerField()
    color = models.CharField(max_length=20)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    car_image = CloudinaryField('image')
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.make} {self.model} ({self.year})'
    
    
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return f"Booking for {self.car} by {self.user}"
    