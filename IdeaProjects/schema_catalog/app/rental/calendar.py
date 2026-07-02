from datetime import date

from .models import Rental


class RentalCalendar:
    """Checks device availability by detecting date range overlaps in active rentals."""

    @staticmethod
    def is_available(device_id: int, start: date, end: date) -> bool:
        return not Rental.objects.filter(
            device_id=device_id,
            status=Rental.Status.ACTIVE,
            start_date__lt=end,
            end_date__gt=start,
        ).exists()

    @staticmethod
    def get_calendar(device_id: int) -> list:
        """Return list of occupied date ranges for a device."""
        return list(
            Rental.objects.filter(
                device_id=device_id,
                status=Rental.Status.ACTIVE,
            ).values("start_date", "end_date", "user_id")
        )
