from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Rental
from .serializers import RentalSerializer
from .services import RentalService


class RentalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rentals = RentalService.get_user_rentals(request.user.id)
        return Response(RentalSerializer(rentals, many=True).data)

    def post(self, request):
        serializer = RentalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            rental = RentalService.rent(
                user_id=request.user.id,
                device_id=serializer.validated_data["device"].id,
                start=serializer.validated_data["start_date"],
                end=serializer.validated_data["end_date"],
            )
            return Response(RentalSerializer(rental).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            rental = RentalService.cancel(pk, request.user.id)
            return Response(RentalSerializer(rental).data)
        except Rental.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, device_id):
        calendar = RentalService.get_calendar(device_id)
        return Response(calendar)