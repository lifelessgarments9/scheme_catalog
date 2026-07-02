from rest_framework import serializers

from .models import Category, Device


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class DeviceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Device
        fields = [
            "id", "name", "description", "image", "documentation",
            "category", "category_name", "manufacturer", "quantity", "is_available",
        ]