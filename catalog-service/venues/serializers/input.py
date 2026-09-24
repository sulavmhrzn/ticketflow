from rest_framework import serializers


class VenueInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=500)
    city = serializers.CharField(max_length=100)


class SeatGenerationInputSerializer(serializers.Serializer):
    section = serializers.CharField(max_length=50)
    rows = serializers.ListField(child=serializers.CharField(max_length=10))
    seats_per_row = serializers.IntegerField(min_value=1, max_value=100)
