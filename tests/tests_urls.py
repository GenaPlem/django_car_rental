from django.test import SimpleTestCase
from django.urls import reverse, resolve
from car_rental.views import (
    HomeView, 
    CarsListView, 
    CarDetailsView, 
    ProfileView, 
    BookingEditView,
    BookingDeleteView,
    PrivacyPolicyView
)


class TestUrls(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomeView)

    def test_cars_list_url_resolves(self):
        url = reverse('cars-list')
        self.assertEquals(resolve(url).func.view_class, CarsListView)

    def test_car_details_url_resolves(self):
        url = reverse('car-details', args=[1])
        self.assertEquals(resolve(url).func.view_class, CarDetailsView)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func.view_class, ProfileView)

    def test_booking_edit_url_resolves(self):
        url = reverse('booking_edit', args=[1])
        self.assertEquals(resolve(url).func.view_class, BookingEditView)

    def test_booking_delete_url_resolves(self):
        url = reverse('booking_delete', args=[1])
        self.assertEquals(resolve(url).func.view_class, BookingDeleteView)

    def test_privacy_policy_url_resolves(self):
        url = reverse('privacy-policy')
        self.assertEquals(resolve(url).func.view_class, PrivacyPolicyView)
        