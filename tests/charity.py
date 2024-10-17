from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from impactreeapi.models import Charity, CharityCategory


class CharityViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.User = get_user_model()

        # Create a regular user
        self.regular_user = self.User.objects.create_user(
            username="regular_user", password="testpass123"
        )

        # Create an admin user
        self.admin_user = self.User.objects.create_user(
            username="admin_user", password="testpass123", is_staff=True
        )

        # Create a test category
        self.category = CharityCategory.objects.create(name="Test Category")

        # Create a test charity
        self.charity = Charity.objects.create(
            name="Test Charity",
            description="Test Description",
            impact_metric="Test Metric",
            impact_ratio=1.0,
            website_url="http://testcharity.com",
            category=self.category,
        )

        self.charity_data = {
            "name": "New Charity",
            "description": "New Description",
            "impact_metric": "New Metric",
            "impact_ratio": 2.0,
            "website_url": "http://newcharity.com",
            "category": self.category.id,
        }

    def test_list_charities(self):
        """Test that any user can list charities"""
        url = "/charities"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_charity(self):
        """Test that any user can retrieve a charity"""
        url = f"/charities/{self.charity.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_charity_as_regular_user(self):
        """Test that a regular user cannot create a charity"""
        self.client.force_authenticate(user=self.regular_user)
        url = "/charities"
        response = self.client.post(url, self.charity_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_charity_as_admin(self):
        """Test that an admin user can create a charity"""
        self.client.force_authenticate(user=self.admin_user)
        url = "/charities"
        response = self.client.post(url, self.charity_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_charity_as_regular_user(self):
        """Test that a regular user cannot update a charity"""
        self.client.force_authenticate(user=self.regular_user)
        url = f"/charities/{self.charity.id}"
        response = self.client.put(url, self.charity_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_charity_as_admin(self):
        """Test that an admin user can update a charity"""
        self.client.force_authenticate(user=self.admin_user)
        url = f"/charities/{self.charity.id}"
        response = self.client.put(url, self.charity_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_charity_as_regular_user(self):
        """Test that a regular user cannot delete a charity"""
        self.client.force_authenticate(user=self.regular_user)
        url = f"/charities/{self.charity.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_charity_as_admin(self):
        """Test that an admin user can delete a charity"""
        self.client.force_authenticate(user=self.admin_user)
        url = f"/charities/{self.charity.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
