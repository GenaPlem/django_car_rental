from django.test import TestCase
from decimal import Decimal
from datetime import date
from car_rental.models import Car, Booking
from django.contrib.auth.models import User


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        car_image_url = 'https://res.cloudinary.com/dd2fwm3fh/image/upload/v1699883191/xgwfa17rshjqvkaxk2hb.webp'
        Car.objects.create(make='Audi',
                           model='A4',
                           year=2020,
                           seats=4,
                           transmission_type='manual',
                           fuel_type='petrol',
                           price_per_day=Decimal('200.00'),
                           car_image=car_image_url,
                           available=True
                           )

    def test_car_attributes(self):
        car = Car.objects.get(id=1)
        expected_url = 'https://res.cloudinary.com/dd2fwm3fh/image/upload/v1699883191/xgwfa17rshjqvkaxk2hb'

        self.assertEqual(car.make, 'Audi')
        self.assertEqual(car.model, 'A4')
        self.assertEqual(car.year, 2020)
        self.assertEqual(car.seats, 4)
        self.assertEqual(car.transmission_type, 'manual')
        self.assertEqual(car.fuel_type, 'petrol')
        self.assertEqual(car.price_per_day, Decimal('200.00'))
        self.assertEqual(car.car_image.url, expected_url)
        self.assertTrue(car.available)

    def test_car__str__(self):
        car = Car.objects.get(id=1)
        expected_str = f'{car.make} {car.model} ({car.year})'
        self.assertEqual(str(car), expected_str)

    def test_transmission_type_choices(self):
        car = Car.objects.get(id=1)
        self.assertIn(car.transmission_type, [choice[0] for choice in Car.TRANSMISSION_CHOICES])

    def test_cloudinary_image_field(self):
        car = Car.objects.get(id=1)
        self.assertIn('res.cloudinary.com', car.car_image.url)
