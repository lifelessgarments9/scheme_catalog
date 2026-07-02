from rest_framework import serializers

from .models import Rental


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ["id", "device", "user", "start_date", "end_date", "status"]
        read_only_fields = ["id", "user", "status"]