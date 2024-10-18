from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/register"
        self.login_url = "/login"
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        user = response.data["user"]
        self.assertEqual(user["username"], self.user_data["username"])
        self.assertEqual(user["email"], self.user_data["email"])
        self.assertEqual(user["first_name"], self.user_data["first_name"])
        self.assertEqual(user["last_name"], self.user_data["last_name"])
        self.assertIn("is_staff", user)
        self.assertFalse(
            user["is_staff"]
        )  # Assuming new users are not staff by default

    def test_login_user(self):
        # First, create a user
        user = User.objects.create_user(**self.user_data)

        # Create a token for the user
        Token.objects.create(user=user)

        # Then, attempt to login
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("valid", response.data)
        self.assertTrue(response.data["valid"])
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        user = response.data["user"]
        self.assertEqual(user["username"], self.user_data["username"])
        self.assertEqual(user["email"], self.user_data["email"])
        self.assertEqual(user["first_name"], self.user_data["first_name"])
        self.assertEqual(user["last_name"], self.user_data["last_name"])
        self.assertIn("is_staff", user)
        self.assertFalse(user["is_staff"])  # Assuming the user is not staff

    # ... rest of the test methods remain the same
