from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOrganizer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "organizer")


class IsVenueOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return str(obj.organizer_id) == str(request.user.id)
