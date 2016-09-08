from rest_framework import permissions
from .utils import get_participant


class IsParticipantOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        participant = get_participant(request)
        if participant:
            return True
        return False
