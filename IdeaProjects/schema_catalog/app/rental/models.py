from django.db import models

from app.accounts.models import User
from app.catalog.models import Device


class Rental(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="rentals")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return f"{self.user} — {self.device} [{self.start_date} / {self.end_date}]"