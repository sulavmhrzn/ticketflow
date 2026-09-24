from venues.models import Seat, Venue


def create_venue(*, name: str, address: str, city: str, organizer_id) -> Venue:
    return Venue.objects.create(
        name=name, address=address, city=city, organizer_id=organizer_id
    )


def update_venue(
    *,
    venue: Venue,
    name: str | None = None,
    address: str | None = None,
    city: str | None = None,
) -> Venue:
    update_fields = []
    if name and venue.name != name:
        venue.name = name
        update_fields.append("name")
    if address and venue.address != address:
        venue.address = address
        update_fields.append("address")
    if city and venue.city != city:
        venue.city = city
        update_fields.append("city")

    if update_fields:
        venue.save(update_fields=[*update_fields, "updated_at"])

    return venue


def generate_seats(
    *, venue: Venue, section: str, rows: list[str], seats_per_row: int
) -> list[Seat]:
    if Seat.objects.filter(venue=venue, section=section).exists():
        raise ValueError(
            f"Section '{section}' already has seats defined for this venue."
        )

    seats = [
        Seat(venue=venue, section=section, row=row, seat_number=str(seat_num))
        for row in rows
        for seat_num in range(1, seats_per_row + 1)
    ]
    return Seat.objects.bulk_create(seats)
