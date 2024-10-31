from django.http import HttpResponseServerError
from rest_framework import serializers, status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from impactreeapi.models import Charity
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
import uuid
import base64
from django.core.files.base import ContentFile


class IsAdminUserOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Custom permission class to allow read-only access to non-admin users
    and full access to admin users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CharityViewSet(ViewSet):
    """Charity view set"""

    permission_classes = [IsAdminUserOrReadOnly]

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized instance
        """
        charity = Charity()

        if "image" in request.data and request.data["image"]:
            format, imgstr = request.data["image"].split(";base64,")
            ext = format.split("/")[-1]
            charity.image = ContentFile(
                base64.b64decode(imgstr), name=f"charity-{uuid.uuid4()}.{ext}"
            )

        charity.name = request.data["name"]
        charity.description = request.data["description"]
        charity.impact_metric = request.data["impact_metric"]
        charity.impact_ratio = request.data["impact_ratio"]
        charity.website_url = request.data["website_url"]

        # Assuming category is sent as an ID
        if "category" in request.data:
            charity.category_id = request.data["category"]

        try:
            charity.save()
            serializer = CharitySerializer(charity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item

        Returns:
            Response -- JSON serialized instance
        """
        try:
            charity = Charity.objects.get(pk=pk)
            serializer = CharitySerializer(charity)
            return Response(serializer.data)
        except Charity.DoesNotExist:
            return Response(
                {"message": "Charity not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return Response({"reason": ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests"""
        try:
            charity = Charity.objects.get(pk=pk)

            if "image" in request.data and request.data["image"]:
                # Only process if it's a new base64 image
                if request.data["image"].startswith("data:"):
                    format, imgstr = request.data["image"].split(";base64,")
                    ext = format.split("/")[-1]
                    charity.image = ContentFile(
                        base64.b64decode(imgstr), name=f"charity-{uuid.uuid4()}.{ext}"
                    )
                # If it's a media URL path, just preserve the existing image
                elif request.data["image"].startswith("/media/"):
                    pass  # Keep existing image, no processing needed

            if "name" in request.data:
                charity.name = request.data["name"]
            if "description" in request.data:
                charity.description = request.data["description"]
            if "impact_metric" in request.data:
                charity.impact_metric = request.data["impact_metric"]
            if "impact_ratio" in request.data:
                charity.impact_ratio = request.data["impact_ratio"]
            if "website_url" in request.data:
                charity.website_url = request.data["website_url"]
            if "category" in request.data:
                charity.category_id = request.data["category"]

            charity.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)

        except Charity.DoesNotExist:
            return Response(
                {"message": "Charity not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item

        Returns:
            Response -- 204, 404, or 500 status code
        """
        try:
            charity = Charity.objects.get(pk=pk)
            charity.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Charity.DoesNotExist:
            return Response(
                {"message": "Charity not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as ex:
            return Response(
                {"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        """Handle GET requests for all items

        Returns:
            Response -- JSON serialized array
        """
        try:
            charities = Charity.objects.all()
            serializer = CharitySerializer(charities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex)


class CharitySerializer(serializers.ModelSerializer):
    """JSON serializer for Charity"""

    class Meta:
        model = Charity
        fields = (
            "id",
            "name",
            "category",
            "description",
            "impact_metric",
            "impact_ratio",
            "website_url",
            "image",
        )
        depth = 1
