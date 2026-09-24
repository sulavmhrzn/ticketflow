from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from venues.models import Venue
from venues.permissions import IsOrganizer, IsVenueOwner
from venues.selectors import list_seats_for_venue, list_venues
from venues.serializers.input import SeatGenerationInputSerializer, VenueInputSerializer
from venues.serializers.output import SeatOutputSerializer, VenueOutputSerializer
from venues.services import create_venue, generate_seats, update_venue


class VenueListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsOrganizer()]
        return [IsAuthenticatedOrReadOnly()]

    def get(self, request: Request) -> Response:
        venues = list_venues()
        return Response(VenueOutputSerializer(venues, many=True).data)

    def post(self, request):
        input_serializer = VenueInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        venue = create_venue(
            **input_serializer.validated_data, organizer_id=request.user.id
        )

        return Response(VenueOutputSerializer(venue).data, status=201)


class VenueDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsVenueOwner]

    def get_object(self, venue_id):
        obj = get_object_or_404(Venue, id=venue_id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, venue_id):
        venue = self.get_object(venue_id)
        return Response(VenueOutputSerializer(venue).data)

    def patch(self, request, venue_id):
        venue = self.get_object(venue_id)
        input_serializer = VenueInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        venue = update_venue(venue=venue, **input_serializer.validated_data)

        return Response(VenueOutputSerializer(venue).data)

    def delete(self, request, venue_id):
        venue = self.get_object(venue_id)
        venue.delete()
        return Response(status=204)


class SeatGenerateView(APIView):
    permission_classes = [IsAuthenticated, IsOrganizer, IsVenueOwner]

    def post(self, request, venue_id):
        venue = get_object_or_404(Venue, id=venue_id)
        self.check_object_permissions(request, venue)

        input_serializer = SeatGenerationInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        try:
            seats = generate_seats(venue=venue, **input_serializer.validated_data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        return Response(SeatOutputSerializer(seats, many=True).data, status=201)


class SeatListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, venue_id):
        seats = list_seats_for_venue(venue_id=venue_id)
        return Response(SeatOutputSerializer(seats, many=True).data)
