from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from datetime import date
from car_rental.models import Car, Booking
from django.contrib.auth.models import User


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
        response = self.client.get(reverse('cars-list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertEqual(len(response.context['cars']), 4)


class CarDetailsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        car_image_url = 'https://res.cloudinary.com/dd2fwm3fh/image/upload/v1699883191/xgwfa17rshjqvkaxk2hb.webp'

        cls.car = Car.objects.create(make='Audi',
                                     model='A4',
                                     year=2020,
                                     seats=4,
                                     transmission_type='manual',
                                     fuel_type='petrol',
                                     price_per_day=Decimal('200.00'),
                                     car_image=car_image_url
                                     )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/cars/{self.car.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('car-details', kwargs={'pk': self.car.pk}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('car-details', kwargs={'pk': self.car.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_details.html')

    def test_context_data(self):
        response = self.client.get(reverse('car-details', kwargs={'pk': self.car.pk}))
        self.assertTrue('form' in response.context)
        self.assertTrue('booked_dates' in response.context)
        self.assertEqual(response.context['car'], self.car)


class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='aSdw12465')
        test_user.save()

        car_image_url = 'https://res.cloudinary.com/dd2fwm3fh/image/upload/v1699883191/xgwfa17rshjqvkaxk2hb.webp'
        test_car = Car.objects.create(make='Audi',
                                      model='A4',
                                      year=2020,
                                      seats=4,
                                      transmission_type='manual',
                                      fuel_type='petrol',
                                      price_per_day=Decimal('200.00'),
                                      car_image=car_image_url
                                      )
        Booking.objects.create(
            user=test_user,
            car=test_car,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 2),
            name='TestName',
            surname='TestSurname',
            child_seat=False,
            insurance_type='standard',
            rules_agreement=True,
            total_price=Decimal('440.00')
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('profile'))
        self.assertTrue(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser', password='aSdw12465')
        response = self.client.get(reverse('profile'))

        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'profile.html')

    def test_only_bookings_for_logged_in_user_are_displayed(self):
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        Booking.objects.create(user=test_user2,
                               car=Car.objects.get(id=1),
                               start_date='2024-01-03',
                               end_date='2024-01-04',
                               name='TestName',
                               surname='TestSurname',
                               child_seat=False,
                               insurance_type='standard',
                               rules_agreement=True,
                               )

        self.client.login(username='testuser', password='aSdw12465')
        response = self.client.get(reverse('profile'))

        self.assertTrue('bookings' in response.context)
        for booking in response.context['bookings']:
            self.assertEqual(response.context['user'], booking.user)


class PrivacyPolicyViewTest(TestCase):
    def test_privacy_policy_view_status_code(self):
        response = self.client.get(reverse('privacy-policy'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_view_uses_correct_template(self):
        response = self.client.get(reverse('privacy-policy'))
        self.assertTemplateUsed(response, 'privacy_policy.html')
