from django.contrib import admin

from venues.models import Seat, Venue


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "city", "organizer_id", "created_at"]
    list_filter = ["city"]
    search_fields = ["name", "city"]
    inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ["venue", "section", "row", "seat_number"]
    list_filter = ["venue", "section"]
    search_fields = ["section", "row", "seat_number"]
