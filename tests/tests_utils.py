from django.test import TestCase
from datetime import datetime
from car_rental.utils import calculate_total_price


class TestCalculateTotalPrice(TestCase):

    def test_basic_rental(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 5)
        price_per_day = 100
        self.assertEqual(calculate_total_price(start_date, end_date, price_per_day, False, 'standard'), 540)

    def test_rental_with_child_seat(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 3)
        price_per_day = 100
        self.assertEqual(calculate_total_price(start_date, end_date, price_per_day, True, 'standard'), 355)

    def test_rental_with_different_insurance_types(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 1, 1)
        price_per_day = 100
        
        self.assertEqual(calculate_total_price(start_date, end_date, price_per_day, False, 'young'), 150)
        self.assertEqual(calculate_total_price(start_date, end_date, price_per_day, False, 'standard'), 140)
        self.assertEqual(calculate_total_price(start_date, end_date, price_per_day, False, 'senior'), 160)
        