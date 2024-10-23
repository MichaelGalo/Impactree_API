from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from impactreeapi.models import ImpactPlan, Milestone, ImpactPlanCharity
from django.db.models import Max


class ImpactPlanViewSet(ViewSet):
    """ImpactPlan view set"""

    def get_appropriate_milestone(self, philanthropy_percentage):
        """Helper method to get the appropriate milestone based on philanthropy percentage"""
        return (
            Milestone.objects.filter(required_percentage__lte=philanthropy_percentage)
            .order_by("-required_percentage")
            .first()
        )

    def create(self, request):
        """Handle POST operations"""
        try:
            user = User.objects.get(pk=request.data["user"])

            # Check if the user already has an impact plan
            existing_plan = ImpactPlan.objects.filter(user=user).first()
            if existing_plan:
                return Response(
                    {"message": "User already has an impact plan."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            impact_plan = ImpactPlan()
            impact_plan.user = User.objects.get(pk=request.data["user"])
            impact_plan.annual_income = request.data["annual_income"]
            impact_plan.philanthropy_percentage = request.data[
                "philanthropy_percentage"
            ]
            impact_plan.total_annual_allocation = request.data[
                "total_annual_allocation"
            ]

            # Automatically set the appropriate milestone
            impact_plan.current_milestone = self.get_appropriate_milestone(
                impact_plan.philanthropy_percentage
            )

            impact_plan.save()

            # Handle charity allocations if provided
            charities_data = request.data.get("charities", [])
            for charity_data in charities_data:
                ImpactPlanCharity.objects.create(
                    impact_plan=impact_plan,
                    charity_id=charity_data["charity_id"],
                    allocation_amount=charity_data["allocation_amount"],
                )

            serializer = ImpactPlanSerializer(impact_plan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single ImpactPlan"""
        try:
            impact_plan = ImpactPlan.objects.prefetch_related(
                "impactplancharity_set", "impactplancharity_set__charity"
            ).get(pk=pk)
            serializer = ImpactPlanSerializer(impact_plan)
            return Response(serializer.data)
        except ImpactPlan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests"""
        try:
            impact_plan = ImpactPlan.objects.get(pk=pk)

            # Check if the update is trying to change the user
            if "user" in request.data and request.data["user"] != impact_plan.user.id:
                return Response(
                    {
                        "message": "Cannot change the user associated with an impact plan."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            impact_plan.annual_income = request.data.get(
                "annual_income", impact_plan.annual_income
            )
            impact_plan.philanthropy_percentage = request.data.get(
                "philanthropy_percentage", impact_plan.philanthropy_percentage
            )
            impact_plan.total_annual_allocation = request.data.get(
                "total_annual_allocation", impact_plan.total_annual_allocation
            )

            # Automatically update the milestone if philanthropy_percentage has changed
            if "philanthropy_percentage" in request.data:
                impact_plan.current_milestone = self.get_appropriate_milestone(
                    impact_plan.philanthropy_percentage
                )

            impact_plan.save()

            # This section handles charity updates
            charities_data = request.data.get("charities")
            if charities_data is not None:
                # Clear existing relationships
                impact_plan.impactplancharity_set.all().delete()
                # Create new ones
                for charity_data in charities_data:
                    ImpactPlanCharity.objects.create(
                        impact_plan=impact_plan,
                        charity_id=charity_data["charity_id"],
                        allocation_amount=charity_data["allocation_amount"],
                    )

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ImpactPlan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single ImpactPlan"""
        try:
            impact_plan = ImpactPlan.objects.get(pk=pk)
            impact_plan.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ImpactPlan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests for all ImpactPlans"""
        try:
            impact_plans = ImpactPlan.objects.prefetch_related(
                "impactplancharity_set", "impactplancharity_set__charity"
            ).all()
            serializer = ImpactPlanSerializer(impact_plans, many=True)
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for User"""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
        )


class ImpactPlanCharitySerializer(serializers.ModelSerializer):
    """JSON serializer for ImpactPlanCharity"""

    class Meta:
        model = ImpactPlanCharity
        fields = ("id", "charity", "allocation_amount")
        depth = 1


class ImpactPlanSerializer(serializers.ModelSerializer):
    """JSON serializer for ImpactPlan"""

    user = UserSerializer(many=False)
    charities = ImpactPlanCharitySerializer(
        source="impactplancharity_set", many=True, read_only=True
    )

    class Meta:
        model = ImpactPlan
        fields = (
            "id",
            "user",
            "annual_income",
            "philanthropy_percentage",
            "total_annual_allocation",
            "current_milestone",
            "charities",
        )
        depth = 1
