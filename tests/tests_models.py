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


class BookingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        car_image_url = 'https://res.cloudinary.com/dd2fwm3fh/image/upload/v1699883191/xgwfa17rshjqvkaxk2hb.webp'
        test_car = Car.objects.create(make='Audi',
                                      model='A4',
                                      year=2020,
                                      seats=4,
                                      transmission_type='manual',
                                      fuel_type='petrol',
                                      price_per_day=Decimal('200.00'),
                                      car_image=car_image_url,
                                      available=True
                                      )

        test_user = User.objects.create(username='testuser', password='aSdw12465')
        Booking.objects.create(
            user=test_user,
            car=test_car,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 3),
            name='TestName',
            surname='TestSurname',
            child_seat=False,
            insurance_type='standard',
            rules_agreement=True,
            total_price=Decimal('640.00')
        )

    def test_booking_creation(self):
        booking = Booking.objects.get(id=1)

        self.assertTrue(isinstance(booking, Booking))

    def test_booking__str__(self):
        booking = Booking.objects.get(id=1)
        expected_str = (f"Booking for {booking.car} by {booking.name} {booking.surname} "
                        f"({booking.user}) from {booking.start_date} to {booking.end_date}. "
                        f"Total price: {booking.total_price}€")

        self.assertEqual(booking.__str__(), expected_str)

    def test_insurance_type_choices(self):
        booking = Booking.objects.get(id=1)
        self.assertIn(booking.insurance_type, [choice[0] for choice in Booking.INSURANCE_CHOICES])
