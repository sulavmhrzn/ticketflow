from rest_framework import serializers

from venues.models import Seat, Venue


class SeatOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = [
            "id",
            "section",
            "row",
            "seat_number",
        ]


class VenueOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            "id",
            "name",
            "address",
            "city",
            "organizer_id",
            "created_at",
            "updated_at",
        ]
