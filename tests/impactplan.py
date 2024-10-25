from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from impactreeapi.models import (
    ImpactPlan,
    Milestone,
    Charity,
    ImpactPlanCharity,
    CharityCategory,
)


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

        # Create charity category first
        self.charity_category = CharityCategory.objects.create(name="Test Category")

        self.charity1 = Charity.objects.create(
            name="Test Charity 1",
            category=self.charity_category,
            description="Test charity 1 description",
            impact_metric="people helped",
            impact_ratio=0.5,
        )
        self.charity2 = Charity.objects.create(
            name="Test Charity 2",
            category=self.charity_category,
            description="Test charity 2 description",
            impact_metric="meals provided",
            impact_ratio=1.0,
        )

        self.impact_plan_data = {
            "user": self.user.id,  # Keep this as user ID for API requests
            "annual_income": 100000.00,
            "philanthropy_percentage": 5.00,
            "total_annual_allocation": 5000.00,
            "charities": [
                {"charity_id": self.charity1.id, "allocation_amount": 2500.00},
                {"charity_id": self.charity2.id, "allocation_amount": 2500.00},
            ],
        }

        # Create a separate dict for direct ORM operations
        self.impact_plan_orm_data = {
            "user": self.user,  # Use the User instance for ORM operations
            "annual_income": 100000.00,
            "philanthropy_percentage": 5.00,
            "total_annual_allocation": 5000.00,
        }

    def test_create_impact_plan(self):
        response = self.client.post(
            "/impactplans", self.impact_plan_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImpactPlan.objects.count(), 1)
        new_plan = ImpactPlan.objects.first()
        self.assertEqual(new_plan.annual_income, 100000.00)
        self.assertEqual(new_plan.philanthropy_percentage, 5.00)
        self.assertEqual(new_plan.total_annual_allocation, 5000.00)
        self.assertEqual(new_plan.current_milestone, self.milestone)
        self.assertEqual(new_plan.impactplancharity_set.count(), 2)

    def test_create_duplicate_impact_plan(self):
        # First, create an impact plan
        self.client.post("/impactplans", self.impact_plan_data, format="json")

        # Attempt to create a second impact plan
        new_impact_plan_data = {
            "user": self.user.id,
            "annual_income": 120000.00,
            "philanthropy_percentage": 5.00,
            "total_annual_allocation": 6000.00,
        }
        response = self.client.post("/impactplans", new_impact_plan_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ImpactPlan.objects.count(), 1)  # Still only one plan

    def test_retrieve_impact_plan(self):
        # Create an impact plan first
        impact_plan = ImpactPlan.objects.create(**self.impact_plan_orm_data)
        # Add charities to the plan
        ImpactPlanCharity.objects.create(
            impact_plan=impact_plan, charity=self.charity1, allocation_amount=2500.00
        )
        ImpactPlanCharity.objects.create(
            impact_plan=impact_plan, charity=self.charity2, allocation_amount=2500.00
        )

        response = self.client.get(f"/impactplans/{impact_plan.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["annual_income"], "100000.00")
        self.assertEqual(response.data["philanthropy_percentage"], "5.00")
        self.assertEqual(response.data["total_annual_allocation"], "5000.00")
        self.assertEqual(response.data["user"]["email"], "testuser@example.com")
        self.assertEqual(response.data["user"]["first_name"], "Test")
        self.assertEqual(response.data["user"]["last_name"], "User")
        self.assertEqual(response.data["user"]["is_staff"], False)
        self.assertEqual(len(response.data["charities"]), 2)
        self.assertEqual(response.data["charities"][0]["allocation_amount"], "2500.00")

    def test_update_impact_plan(self):
        # Create an impact plan first
        impact_plan = ImpactPlan.objects.create(**self.impact_plan_orm_data)
        updated_data = {
            "annual_income": 75000.00,
            "philanthropy_percentage": 5.00,
            "total_annual_allocation": 3750.00,
            "charities": [
                {"charity_id": self.charity1.id, "allocation_amount": 3750.00}
            ],
        }
        response = self.client.put(
            f"/impactplans/{impact_plan.id}", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify response data
        self.assertEqual(response.data["annual_income"], "75000.00")
        self.assertEqual(response.data["philanthropy_percentage"], "5.00")
        self.assertEqual(response.data["total_annual_allocation"], "3750.00")
        self.assertEqual(len(response.data["charities"]), 1)
        self.assertEqual(response.data["charities"][0]["allocation_amount"], "3750.00")

        # Verify database was updated
        impact_plan.refresh_from_db()
        self.assertEqual(impact_plan.annual_income, 75000.00)
        self.assertEqual(impact_plan.philanthropy_percentage, 5.00)
        self.assertEqual(impact_plan.total_annual_allocation, 3750.00)
        self.assertEqual(impact_plan.current_milestone, self.milestone)
        self.assertEqual(impact_plan.impactplancharity_set.count(), 1)
        self.assertEqual(
            impact_plan.impactplancharity_set.first().allocation_amount, 3750.00
        )

    def test_list_impact_plans(self):
        # Create an impact plan first
        impact_plan = ImpactPlan.objects.create(**self.impact_plan_orm_data)
        ImpactPlanCharity.objects.create(
            impact_plan=impact_plan, charity=self.charity1, allocation_amount=5000.00
        )

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
        self.assertEqual(len(response.data[0]["charities"]), 1)
        self.assertEqual(
            response.data[0]["charities"][0]["allocation_amount"], "5000.00"
        )

    def test_delete_impact_plan(self):
        # Create an impact plan first
        impact_plan = ImpactPlan.objects.create(**self.impact_plan_orm_data)
        ImpactPlanCharity.objects.create(
            impact_plan=impact_plan, charity=self.charity1, allocation_amount=2500.00
        )

        response = self.client.delete(f"/impactplans/{impact_plan.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ImpactPlan.objects.count(), 0)
        self.assertEqual(
            ImpactPlanCharity.objects.count(), 0
        )  # Verify cascading delete

    def test_update_impact_plan_remove_all_charities(self):
        """Test removing all charities from an impact plan"""
        # Create plan with charities first
        impact_plan = ImpactPlan.objects.create(**self.impact_plan_orm_data)
        ImpactPlanCharity.objects.create(
            impact_plan=impact_plan, charity=self.charity1, allocation_amount=2500.00
        )

        # Update to remove all charities
        updated_data = {"charities": []}

        response = self.client.put(
            f"/impactplans/{impact_plan.id}", updated_data, format="json"
        )
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )  # Changed from 204 to 200

        # Verify charities were removed
        response = self.client.get(f"/impactplans/{impact_plan.id}")
        self.assertEqual(len(response.data["charities"]), 0)
