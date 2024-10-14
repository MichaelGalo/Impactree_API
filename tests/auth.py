import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AuthTests(APITestCase):
    def setUp(self) -> None:
        """
        Set up test data
        """
        self.register_url = "/register"
        self.login_url = "/login"
        self.user_data = {
            "username": "stevebrownlee",
            "email": "steve@stevebrownlee.com",
            "password": "Admin8*",
            "first_name": "Steve",
            "last_name": "Brownlee",
        }

    def test_register_user(self):
        """
        Ensure we can register a new user and a token is created.
        """
        response = self.client.post(self.register_url, self.user_data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", json_response)

        # Verify user creation
        user = User.objects.get(username=self.user_data["username"])
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user_data["email"])

        # Verify token creation
        token = Token.objects.get(user=user)
        self.assertIsNotNone(token)

        # Test for duplicate username
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test for missing fields
        incomplete_data = self.user_data.copy()
        del incomplete_data["username"]
        response = self.client.post(self.register_url, incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        """
        Ensure we can login a user and get a token.
        """
        # Register a user first
        self.client.post(self.register_url, self.user_data, format="json")

        # Login with correct credentials
        login_data = {
            "username": self.user_data["username"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", json_response)
        self.assertTrue(json_response["valid"])

        # Verify the token matches the one created at registration
        user = User.objects.get(username=self.user_data["username"])
        token = Token.objects.get(user=user)
        self.assertEqual(json_response["token"], token.key)

        # Test login with incorrect password
        login_data["password"] = "wrongpassword"
        response = self.client.post(self.login_url, login_data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(json_response["valid"])

        # Test login with non-existent user
        login_data["username"] = "nonexistentuser"
        response = self.client.post(self.login_url, login_data, format="json")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(json_response["valid"])
