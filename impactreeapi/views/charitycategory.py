from rest_framework import viewsets, serializers
from impactreeapi.models import CharityCategory


class CharityCategoryViewSet(viewsets.ModelViewSet):
    queryset = CharityCategory.objects.all()

    class CharityCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = CharityCategory
            fields = ["id", "name"]

    serializer_class = CharityCategorySerializer
