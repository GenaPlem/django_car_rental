from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from car_rental.models import Car


class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'index.html')


class CarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_cars = 10
        car_image_url = 'https://res.cloudinary.com/dd2fwm3fh/image/upload/v1699883191/xgwfa17rshjqvkaxk2hb.webp'

        for car in range(number_of_cars):
            Car.objects.create(make='Audi',
                               model='A4',
                               year=2020,
                               seats=4,
                               transmission_type='manual',
                               fuel_type='petrol',
                               price_per_day=Decimal('200.00'),
                               car_image=car_image_url
                               )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/cars/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('cars-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cars.html')

    def test_pagination_is_six(self):
        response = self.client.get(reverse('cars-list'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['cars']), 6)

    def test_lists_all_cars(self):
        response = self.client.get(reverse('cars-list')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['cars']), 4)
