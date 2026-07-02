from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from .serializers import DeviceSerializer
from .services import CatalogService


class DeviceListView(APIView):
    """GET /api/catalog/  — list + filter; POST — create (admin)."""

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request):
        params = request.query_params.dict()
        devices = CatalogService.get_all(filters=params or None)
        return Response(DeviceSerializer(devices, many=True).data)

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device = CatalogService.create(dict(serializer.validated_data))
        return Response(DeviceSerializer(device).data, status=status.HTTP_201_CREATED)


class DeviceDetailView(APIView):
    """GET /api/catalog/<pk>/  PUT  DELETE."""

    def get_permissions(self):
        if self.request.method in ("PUT", "DELETE"):
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request, pk):
        try:
            device = CatalogService.get(pk)
            return Response(DeviceSerializer(device).data)
        except Exception:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        device = CatalogService.update(pk, request.data.dict())
        return Response(DeviceSerializer(device).data)

    def delete(self, request, pk):
        CatalogService.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)