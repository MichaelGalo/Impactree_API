from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from impactreeapi.models import ImpactPlan, Charity, ImpactPlanCharity
from django.urls import reverse
from rest_framework.authtoken.models import Token


class ImpactPlanCharityViewSetTests(APITestCase):

    def setUp(self):
        """Set up required test data"""
        self.client = APIClient()  # Initialize API client
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token = Token.objects.create(user=self.user)  # Create token for user
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + self.token.key
        )  # Authenticate client

        self.impact_plan = ImpactPlan.objects.create(
            user=self.user,
            annual_income=50000,
            philanthropy_percentage=5,
            total_annual_allocation=2500,
        )

        self.charity1 = Charity.objects.create(
            name="Charity1",
            description="Test charity 1",
            impact_ratio=4.0,
        )
        self.charity2 = Charity.objects.create(
            name="Charity2",
            description="Test charity 2",
            impact_ratio=3.5,
        )

    def test_create_impact_plan_charity(self):
        """Test creating a new ImpactPlanCharity"""
        url = reverse("impactplan_charities-list")
        data = {
            "impact_plan_id": self.impact_plan.id,
            "charity_id": self.charity1.id,
            "allocation_amount": 500,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["impact_plan"]["id"], self.impact_plan.id)
        self.assertEqual(response.data["charity"]["id"], self.charity1.id)
        self.assertEqual(float(response.data["allocation_amount"]), 500.00)

    def test_create_duplicate_impact_plan_charity(self):
        """Test creating an ImpactPlanCharity that already exists"""
        ImpactPlanCharity.objects.create(
            impact_plan=self.impact_plan, charity=self.charity1, allocation_amount=500
        )
        url = reverse("impactplan_charities-list")
        data = {
            "impact_plan_id": self.impact_plan.id,
            "charity_id": self.charity1.id,
            "allocation_amount": 500,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"], "This charity is already in the impact plan"
        )

    def test_update_allocation_amount(self):
        """Test updating the allocation amount for an ImpactPlanCharity"""
        impact_plan_charity = ImpactPlanCharity.objects.create(
            impact_plan=self.impact_plan, charity=self.charity1, allocation_amount=500
        )
        url = reverse("impactplan_charities-detail", args=[impact_plan_charity.id])
        data = {"allocation_amount": 750}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["allocation_amount"]), 750.00)

    def test_update_with_missing_allocation_amount(self):
        """Test updating without allocation_amount in the request"""
        impact_plan_charity = ImpactPlanCharity.objects.create(
            impact_plan=self.impact_plan, charity=self.charity1, allocation_amount=500
        )
        url = reverse("impactplan_charities-detail", args=[impact_plan_charity.id])
        data = {}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "allocation_amount is required")

    def test_destroy_impact_plan_charity(self):
        """Test deleting an ImpactPlanCharity"""
        impact_plan_charity = ImpactPlanCharity.objects.create(
            impact_plan=self.impact_plan, charity=self.charity1, allocation_amount=500
        )
        url = reverse("impactplan_charities-detail", args=[impact_plan_charity.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            ImpactPlanCharity.objects.filter(id=impact_plan_charity.id).exists()
        )

    def test_list_impact_plan_charities(self):
        """Test listing ImpactPlanCharities for a user"""
        # Create ImpactPlanCharity relationships
        ImpactPlanCharity.objects.create(
            impact_plan=self.impact_plan, charity=self.charity1, allocation_amount=500
        )
        ImpactPlanCharity.objects.create(
            impact_plan=self.impact_plan, charity=self.charity2, allocation_amount=300
        )

        # Perform the list request
        url = reverse("impactplan_charities-list")
        response = self.client.get(url)

        # Validate the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate that the response data contains expected entries
        self.assertGreater(len(response.data), 0, "Expected non-empty response data")

        # Check that the returned data includes the created relationships
        returned_ids = {item["id"] for item in response.data}
        self.assertIn(
            self.charity1.id, returned_ids, "Charity 1 not found in response data"
        )
        self.assertIn(
            self.charity2.id, returned_ids, "Charity 2 not found in response data"
        )
