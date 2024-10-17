from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from impactreeapi.models import CharityCategory


class CharityCategoryViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.category1 = CharityCategory.objects.create(name="Education")
        self.category2 = CharityCategory.objects.create(name="Healthcare")

    def test_list_charity_categories(self):
        url = "/charitycategories"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_charity_category(self):
        url = f"/charitycategories/{self.category1.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Education")
