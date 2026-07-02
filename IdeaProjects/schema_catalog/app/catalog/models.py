from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Device(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="devices/images/", null=True, blank=True)
    documentation = models.FileField(upload_to="devices/docs/", null=True, blank=True)
    doc_text = models.TextField(blank=True, default="")  # cached parsed text for AI context
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="devices"
    )
    manufacturer = models.CharField(max_length=255, blank=True, default="")
    quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name