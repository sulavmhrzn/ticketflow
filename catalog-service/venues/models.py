import uuid

from django.db import models


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)

    organizer_id = models.UUIDField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Seat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="seats")

    section = models.CharField(max_length=50)
    row = models.CharField(max_length=10)
    seat_number = models.CharField(max_length=10)

    class Meta:
        unique_together = ("venue", "section", "row", "seat_number")
        ordering = ["section", "row", "seat_number"]

    def __str__(self):
        return f"{self.venue.name} - {self.section}{self.row} - {self.seat_number}"
