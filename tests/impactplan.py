from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from impactreeapi.models import ImpactPlan, Milestone


class ImpactPlanViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            is_staff=False,
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.milestone = Milestone.objects.create(
            name="Test Milestone",
            description="A test milestone",
            required_percentage=5.00,
            image_url="https://example.com/image.jpg",
        )

        self.impact_plan_data = {
            "user": self.user,
            "annual_income": 100000.00,
            "philanthropy_percentage": 5.00,
            "total_annual_allocation": 5000.00,
        }
        self.impact_plan = ImpactPlan.objects.create(**self.impact_plan_data)

    def test_create_impact_plan(self):
        new_impact_plan_data = {
            "user": self.user.id,
            "annual_income": 120000.00,
            "philanthropy_percentage": 5.00,
            "total_annual_allocation": 6000.00,
        }
        response = self.client.post("/impactplans", new_impact_plan_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImpactPlan.objects.count(), 2)
        new_plan = ImpactPlan.objects.get(annual_income=120000.00)
        self.assertEqual(new_plan.philanthropy_percentage, 5.00)
        self.assertEqual(new_plan.current_milestone, self.milestone)

    def test_retrieve_impact_plan(self):
        response = self.client.get(f"/impactplans/{self.impact_plan.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["annual_income"], "100000.00")
        self.assertEqual(response.data["philanthropy_percentage"], "5.00")
        self.assertEqual(response.data["total_annual_allocation"], "5000.00")
        self.assertEqual(response.data["user"]["email"], "testuser@example.com")
        self.assertEqual(response.data["user"]["first_name"], "Test")
        self.assertEqual(response.data["user"]["last_name"], "User")
        self.assertEqual(response.data["user"]["is_staff"], False)

    def test_update_impact_plan(self):
        updated_data = {
            "annual_income": 75000.00,
            "philanthropy_percentage": 5.00,
            "total_annual_allocation": 3750.00,
        }
        response = self.client.put(
            f"/impactplans/{self.impact_plan.id}", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.impact_plan.refresh_from_db()
        self.assertEqual(self.impact_plan.annual_income, 75000.00)
        self.assertEqual(self.impact_plan.philanthropy_percentage, 5.00)
        self.assertEqual(self.impact_plan.total_annual_allocation, 3750.00)
        self.assertEqual(self.impact_plan.current_milestone, self.milestone)

    def test_list_impact_plans(self):
        response = self.client.get("/impactplans")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["annual_income"], "100000.00")
        self.assertEqual(response.data[0]["philanthropy_percentage"], "5.00")
        self.assertEqual(response.data[0]["total_annual_allocation"], "5000.00")
        self.assertEqual(response.data[0]["user"]["email"], "testuser@example.com")
        self.assertEqual(response.data[0]["user"]["first_name"], "Test")
        self.assertEqual(response.data[0]["user"]["last_name"], "User")
        self.assertEqual(response.data[0]["user"]["is_staff"], False)

    def test_delete_impact_plan(self):
        response = self.client.delete(f"/impactplans/{self.impact_plan.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ImpactPlan.objects.count(), 0)
