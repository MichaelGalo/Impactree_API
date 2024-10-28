from django.http import HttpResponseServerError
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from impactreeapi.models import ImpactPlanCharity, ImpactPlan, Charity


class ImpactPlanCharityViewSet(ViewSet):
    """ViewSet for handling ImpactPlanCharity operations"""

    def create(self, request):
        """Handle POST operations for adding a charity to an impact plan"""
        try:
            # Get the related objects
            impact_plan = ImpactPlan.objects.get(pk=request.data["impact_plan_id"])
            charity = Charity.objects.get(pk=request.data["charity_id"])

            # Check if relationship already exists
            existing_relation = ImpactPlanCharity.objects.filter(
                impact_plan=impact_plan, charity=charity
            ).first()

            if existing_relation:
                return Response(
                    {"message": "This charity is already in the impact plan"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the new relationship
            impact_plan_charity = ImpactPlanCharity.objects.create(
                impact_plan=impact_plan,
                charity=charity,
                allocation_amount=request.data["allocation_amount"],
            )

            serializer = ImpactPlanCharitySerializer(impact_plan_charity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ImpactPlan.DoesNotExist:
            return Response(
                {"message": "Impact Plan not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Charity.DoesNotExist:
            return Response(
                {"message": "Charity not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, pk=None):
        """Handle PUT requests for updating allocation amount"""
        try:
            impact_plan_charity = ImpactPlanCharity.objects.get(pk=pk)

            # Only allow updating the allocation_amount
            if "allocation_amount" in request.data:
                impact_plan_charity.allocation_amount = request.data[
                    "allocation_amount"
                ]
                impact_plan_charity.save()

                serializer = ImpactPlanCharitySerializer(impact_plan_charity)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "allocation_amount is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ImpactPlanCharity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response(
                {"message": str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single ImpactPlanCharity relationship"""
        try:
            impact_plan_charity = ImpactPlanCharity.objects.get(pk=pk)
            impact_plan_charity.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ImpactPlanCharity.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests for ImpactPlanCharities filtered by user"""
        try:
            # Get the user's impact plan first
            impact_plan = ImpactPlan.objects.get(user=request.auth.user)

            # Then get only the charity relationships for that plan
            impact_plan_charities = ImpactPlanCharity.objects.filter(
                impact_plan=impact_plan
            )

            serializer = ImpactPlanCharitySerializer(impact_plan_charities, many=True)
            return Response(serializer.data)
        except ImpactPlan.DoesNotExist:
            return Response(
                {"message": "No impact plan found for this user"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as ex:
            return HttpResponseServerError(ex)


class ImpactPlanCharitySerializer(serializers.ModelSerializer):
    """JSON serializer for ImpactPlanCharity"""

    class Meta:
        model = ImpactPlanCharity
        fields = ("id", "impact_plan", "charity", "allocation_amount")
        depth = 1
