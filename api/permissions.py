from rest_framework.permissions import BasePermission

class IsOrganizer(BasePermission):
    message = "You are not the organizer of this event. Go away!"

    def has_object_permission(self, request, view, obj):
        if obj.organizer == request.user:
            return True
        return False