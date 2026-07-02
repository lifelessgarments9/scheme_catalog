from django.db.models import QuerySet


class DeviceFilter:
    """Applies query-param filters to a Device queryset."""

    def __init__(self, queryset: QuerySet, params: dict):
        self.queryset = queryset
        self.params = params

    def apply(self) -> QuerySet:
        qs = self.queryset

        if category := self.params.get("category"):
            qs = qs.filter(category__name__iexact=category)

        if manufacturer := self.params.get("manufacturer"):
            qs = qs.filter(manufacturer__icontains=manufacturer)

        if "is_available" in self.params:
            flag = self.params["is_available"].lower() == "true"
            qs = qs.filter(is_available=flag)

        if min_qty := self.params.get("min_quantity"):
            qs = qs.filter(quantity__gte=int(min_qty))

        if search := self.params.get("search"):
            qs = qs.filter(name__icontains=search) | qs.filter(description__icontains=search)

        return qs
