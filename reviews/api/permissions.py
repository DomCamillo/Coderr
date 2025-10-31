from rest_framework import permissions
from rest_framework.response import Response


class isReviewOwner(permissions.BasePermission):
    """Only the Reviewer can customize and delete his Review"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user

class IsCustomer(permissions.BasePermission):

    message = "Nur Customer können Bewertungen erstellen"

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'profile') and
            request.user.profile.type == 'customer'
        )