from django.core.cache import cache

from .models import Device, Category
from .parser import DocumentParser
from .filters import DeviceFilter

CACHE_KEY = "catalog:all"
CACHE_TTL = 300  # 5 minutes


class CatalogService:

    @staticmethod
    def get_all(filters: dict = None):
        """Return all devices, applying optional filters. Caches unfiltered result."""
        if not filters:
            cached = cache.get(CACHE_KEY)
            if cached is not None:
                return cached

        qs = Device.objects.select_related("category").all()

        if filters:
            qs = DeviceFilter(qs, filters).apply()
            return qs

        result = list(qs)
        cache.set(CACHE_KEY, result, CACHE_TTL)
        return result

    @staticmethod
    def get(pk: int) -> Device:
        return Device.objects.select_related("category").get(pk=pk)

    @staticmethod
    def create(data: dict) -> Device:
        category_id = data.pop("category", None)
        device = Device(**data)
        if category_id:
            device.category = Category.objects.get(pk=category_id)
        device.save()
        if device.documentation:
            CatalogService._store_doc_text(device)
        cache.delete(CACHE_KEY)
        return device

    @staticmethod
    def update(pk: int, data: dict) -> Device:
        Device.objects.filter(pk=pk).update(**data)
        cache.delete(CACHE_KEY)
        return Device.objects.select_related("category").get(pk=pk)

    @staticmethod
    def delete(pk: int) -> None:
        Device.objects.filter(pk=pk).delete()
        cache.delete(CACHE_KEY)

    @staticmethod
    def _store_doc_text(device: Device) -> None:
        """Parse documentation file and cache the text on the model."""
        text = DocumentParser.parse(device.documentation.path)
        Device.objects.filter(pk=device.pk).update(doc_text=text)
        device.doc_text = text