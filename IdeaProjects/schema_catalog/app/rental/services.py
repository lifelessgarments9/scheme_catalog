from datetime import date

from .calendar import RentalCalendar
from .models import Rental


class RentalService:

    @staticmethod
    def rent(user_id: int, device_id: int, start: date, end: date) -> Rental:
        if start >= end:
            raise ValueError("start_date must be before end_date")
        if not RentalCalendar.is_available(device_id, start, end):
            raise ValueError("Device is not available for the selected dates")
        return Rental.objects.create(
            user_id=user_id,
            device_id=device_id,
            start_date=start,
            end_date=end,
        )

    @staticmethod
    def cancel(rental_id: int, user_id: int) -> Rental:
        rental = Rental.objects.get(pk=rental_id, user_id=user_id)
        if rental.status != Rental.Status.ACTIVE:
            raise ValueError("Only active rentals can be cancelled")
        rental.status = Rental.Status.CANCELLED
        rental.save(update_fields=["status"])
        return rental

    @staticmethod
    def get_calendar(device_id: int) -> list:
        return RentalCalendar.get_calendar(device_id)

    @staticmethod
    def get_user_rentals(user_id: int):
        return Rental.objects.filter(user_id=user_id).select_related("device").order_by("-start_date")