from venues.models import Seat, Venue


def get_venue_by_id(*, venue_id) -> Venue | None:
    return Venue.objects.filter(id=venue_id).first()


def list_venues():
    return Venue.objects.all()


def list_seats_for_venue(*, venue_id) -> list[Seat]:
    return Seat.objects.filter(venue_id=venue_id)
