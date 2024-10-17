from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from impactreeapi.models import Charity, CharityCategory


class CharityViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.category = CharityCategory.objects.create(name="Test Category")
        self.charity_data = {
            "name": "Test Charity",
            "category": self.category,  # Use the category instance, not its ID
            "description": "A test charity",
            "impact_metric": "Lives improved",
            "impact_ratio": 0.85,
            "website_url": "https://testcharity.org",
        }
        self.charity = Charity.objects.create(**self.charity_data)

    def test_create_charity(self):
        new_charity_data = {
            "name": "New Test Charity",
            "category": self.category.id,  # Use ID for API requests
            "description": "A new test charity",
            "impact_metric": "Dollars saved",
            "impact_ratio": 0.75,
            "website_url": "https://newtestcharity.org",
        }
        response = self.client.post("/charities", new_charity_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Charity.objects.count(), 2)
        self.assertEqual(
            Charity.objects.get(name="New Test Charity").description,
            "A new test charity",
        )

    def test_retrieve_charity(self):
        response = self.client.get(f"/charities/{self.charity.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Charity")

    def test_update_charity(self):
        updated_data = {
            "name": "Updated Test Charity",
            "category": self.category.id,  # Use ID for API requests
            "description": "An updated test charity",
            "impact_metric": "People helped",
            "impact_ratio": 0.9,
            "website_url": "https://updatedtestcharity.org",
        }
        response = self.client.put(
            f"/charities/{self.charity.id}", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.charity.refresh_from_db()
        self.assertEqual(self.charity.name, "Updated Test Charity")
        self.assertEqual(self.charity.description, "An updated test charity")

    def test_list_charities(self):
        response = self.client.get("/charities")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Charity")

    def test_delete_charity(self):
        response = self.client.delete(f"/charities/{self.charity.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Charity.objects.count(), 0)
