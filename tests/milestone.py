# tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from impactreeapi.models import Milestone

User = get_user_model()


class MilestoneViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

        # Updated to use image_filename instead of image_url
        self.milestone1 = Milestone.objects.create(
            name="Test Milestone 1",
            description="Description for Test Milestone 1",
            required_percentage=50.00,
            image_filename="seed-planter.png",  # Using actual filename from your public folder
        )
        self.milestone2 = Milestone.objects.create(
            name="Test Milestone 2",
            description="Description for Test Milestone 2",
            required_percentage=75.00,
            image_filename="sprout-nurturer.png",  # Using actual filename from your public folder
        )

    def test_list_milestones(self):
        url = reverse("milestone-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], self.milestone1.name)
        self.assertEqual(response.data[1]["name"], self.milestone2.name)

    def test_retrieve_milestone(self):
        url = reverse("milestone-detail", kwargs={"pk": self.milestone1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.milestone1.name)
        self.assertEqual(response.data["description"], self.milestone1.description)
        self.assertEqual(
            float(response.data["required_percentage"]),
            self.milestone1.required_percentage,
        )
        # Updated to check image_filename instead of image_url
        self.assertEqual(
            response.data["image_filename"], self.milestone1.image_filename
        )
