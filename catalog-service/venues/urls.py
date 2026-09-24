from django.urls import path

from venues.views import (
    SeatGenerateView,
    SeatListView,
    VenueDetailView,
    VenueListCreateView,
)

urlpatterns = [
    path("venues/", VenueListCreateView.as_view(), name="venue-list-create"),
    path("venues/<uuid:venue_id>/", VenueDetailView.as_view(), name="venue-detail"),
    path("venues/<uuid:venue_id>/seats/", SeatListView.as_view(), name="seat-list"),
    path(
        "venues/<uuid:venue_id>/seats/generate/",
        SeatGenerateView.as_view(),
        name="seat-generate",
    ),
]
