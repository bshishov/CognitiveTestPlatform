from rest_framework import permissions
from cognitive_tests import models


class IsParticipantOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        participant = models.Participant.from_request(request)
        if participant:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participant'):
            if obj.participant.pk == models.Participant.from_request(request).pk:
                return True
        return False


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user and request.user.is_staff:
            return True
        return False


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.is_staff
        return False


class IsParticipantOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'current':
            return True

        if request.user:
            if request.user.is_staff:
                return True

        participant = models.Participant.from_request(request)
        if participant:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'current':
            return True

        if request.user:
            if request.user.is_staff:
                return True

        participant = models.Participant.from_request(request)
        if participant:
            return True
        return False
